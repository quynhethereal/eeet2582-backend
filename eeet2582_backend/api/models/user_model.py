from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, id, email, **extra_fields):
        if not id:
            raise ValueError('Users must have an id')
        elif not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model( id=id, email=email, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.TextField(max_length=500,unique=True, primary_key=True)
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

