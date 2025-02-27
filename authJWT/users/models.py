# from django.db import models
# from django.contrib.auth.models import AbstractUser, Group, Permission


# class User(AbstractUser):
     
#      groups = models.ManyToManyField(Group, related_name="custom_user_set")
#      user_permissions = models.ManyToManyField(Permission, related_name="custom_permission_set")      

#      name=models.CharField(max_length=255 , unique=True)
#      email=models.EmailField(unique=True)
#      password=models.CharField(max_length=255)
#      username=None

#      USERNAME_FIELD='name'
#      REQUIRED_FIELDS=[]


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name, email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Removing default username field
    name = models.CharField(max_length=255, unique=True)  # Custom username field
    email = models.EmailField(unique=True)

    objects = UserManager()  # Set custom manager

    USERNAME_FIELD = 'name'  # Set name as unique identifier
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name
