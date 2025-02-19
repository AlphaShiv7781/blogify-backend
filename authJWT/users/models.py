from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
     
     groups = models.ManyToManyField(Group, related_name="custom_user_set")
     user_permissions = models.ManyToManyField(Permission, related_name="custom_permission_set")      

     name=models.CharField(max_length=255)
     email=models.EmailField(unique=True)
     password=models.CharField(max_length=255)
     username=None

     USERNAME_FIELD='email'
     REQUIRED_FIELDS=[]