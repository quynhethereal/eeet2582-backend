from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, id, email, password=None, **extra_fields):
        if not id:
            raise ValueError('Users must have an id')
        elif not email:
            raise ValueError('Users must have an email address')

        user = self.model(id=id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.TextField(max_length=500, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    objects = UserManager()

    def set_password(self, password):
        # Implement password hashing here
        self.password = password

    def check_password(self, password):
        # Implement password check here
        return self.password == password

    def __str__(self):
        return self.email