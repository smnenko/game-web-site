from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.models import AbstractModel
from user.managers import UserManager


class CustomUser(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=16)
    email = models.EmailField(unique=True, null=True)

    is_email_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class Profile(AbstractModel):
    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(upload_to='users')
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username.capitalize()}\' profile"
