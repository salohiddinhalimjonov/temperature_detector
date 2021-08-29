from django.contrib.auth.models import BaseUserManager
from django.core import validators

class UserManager(BaseUserManager):

    def save_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    def create_activeuser(self, email, password=None, **extra_fields):
        extra_fields['is_superuser']=False
        extra_fields['is_staff']=True
        return self.save_user(email, password, **extra_fields)

    def create_superuser(self, email,password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser should be True')
        extra_fields['is_staff'] = True
        return self.save_user(email, password, **extra_fields)
#I should research this theme completely. Because it is one of the most important part