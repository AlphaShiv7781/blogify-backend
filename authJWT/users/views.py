from rest_framework.views import APIView, Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

from rest_framework.response import Response
import jwt, datetime
from django.conf import settings


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        #
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # JWT payload
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),  
            'iat': datetime.datetime.utcnow()  
        }

        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        
        response = Response()
        # response.set_cookie(
        #     key='jwt',          # Cookie name
        #     value=token,        # Token value
        #     httponly=True,      # Prevent client-side JavaScript from accessing the cookie
        #     secure=False,       # Set to True if using HTTPS
        #     samesite='Lax',     # Helps prevent CSRF attacks
        #     path='/'            # Cookie accessible for all routes
        # )

        # Add token data to the response body
        response.data = {
            'jwt': token
        }
        
        print(response.data)

        return response



class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(f"JWT token from cookie: {token}")

        if not token:
            raise AuthenticationFailed('Token not found')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
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
       

