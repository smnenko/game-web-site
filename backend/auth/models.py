from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(User):
    id = models.IntegerField(primary_key=True, unique=True)
    username = models.OneToOneField(to=User, max_length=32)
    email = models.EmailField()
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    birthday = models.DateField(default=date.today)


@receiver(signal=post_save, sender=User)
def create_user_profile(sender, instance, created):
    if created:
        Profile.objects.create(user=instance)


@receiver(signal=post_save, sender=User)
def save_user_profile(sender, instance):
    instance.profile.save()
