from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from imagekit.models.fields import ImageSpecField
from imagekit.processors import Adjust, ResizeToFill

from .managers import UserManager


class Avatar(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, default='1')
    avatar = models.ImageField(upload_to='users', default='users/default.jpg')
    avatar_small = ImageSpecField(format='JPEG', source='avatar', processors=[
        Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(40, 40)
    ], options={'quality': 90})
    avatar_medium = ImageSpecField(format='JPEG', source='avatar', processors=[
        Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(250, 250)
    ], options={'quality': 90})
    avatar_large = ImageSpecField(format='JPEG', source='avatar', processors=[
        ResizeToFill(500, 500)
    ], options={'quality': 100})
    date_uploaded = models.DateField(default=timezone.now)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=16)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    birth_date = models.DateField(auto_now=False, null=True)
    avatar = models.ForeignKey(to=Avatar, on_delete=models.CASCADE, default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


