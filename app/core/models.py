from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                PermissionsMixin


class UserManager(BaseUserManager):

    # We give the password a default value in case you create users without
    # password
    #
    # Take any extra functions and pass them into Extra fileds. This allows us
    # to add new function arguments without having to edit this function itself
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # This will encrypt the password.
        # part of 'AbstractBaseUser'
        user.save(using=self._db)  # good practise

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):  # inherrit the defines classes
    # Note: 'is_superuser' feild is included as part of the PermissionsMixin
    """Customer user model that supports using email instad of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
