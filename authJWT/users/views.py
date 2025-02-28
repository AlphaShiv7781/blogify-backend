from django.utils import timezone
from rest_framework.views import APIView, Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.response import Response
import jwt, datetime
from django.conf import settings


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # JWT payload
        payload = {
          'id': user.id,
          'name': user.name,
          'email': user.email,
          'exp': timezone.now() + timezone.timedelta(minutes=60),
          'iat': timezone.now()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            
        response = Response({"token": token})
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            secure=False,  # Keep False for local development
            samesite="Lax",  # Changed from None
            path="/",
            # domain="localhost"  # Remove this line
        )
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Credentials"] = "true"
        return response



class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(f"JWT token from cookie: {token}")

        if not token:
            raise AuthenticationFailed('Token not found')

        try:

            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256'],
                options={'leeway': 10}  # Add 10-second grace period
            ) 

            
            print(f"Decoded Payload: {payload}")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed('User not found')

        serializer = UserSerializer(user)
        return Response(serializer.data)




class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response     
       

