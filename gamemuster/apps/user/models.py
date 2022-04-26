from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from imagekit.models.fields import ImageSpecField
from imagekit.processors import Adjust, ResizeToFill

from user.managers import UserManager
from core.models import AbstractModel


class Avatar(AbstractModel):
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


class CustomUser(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=16)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    birth_date = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)

    avatar = models.ForeignKey(to=Avatar, on_delete=models.CASCADE, default=1)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
