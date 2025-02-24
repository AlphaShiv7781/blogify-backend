from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta: # Meta information about serializer
        model = User  #this comes from models.py
        fields = ['id','name','email','password'] #fields to be serialized
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  # Hash the password correctly
        instance.save()
        return instance


       