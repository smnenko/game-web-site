from django.contrib.auth.base_user import BaseUserManager

from django.utils.timezone import now
from django.contrib.auth.models import Group

from user import models


class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, email=extra_fields.get('email'))
        user.set_password(password)
        user.save()

        models.Profile.objects.create(
            user=user,
            first_name=extra_fields.get('first_name'),
            last_name=extra_fields.get('last_name'),
            birth_date=extra_fields.get('birth_date'),
        )

        user_group = Group.objects.filter(name='Users')
        if user_group.exists():
            user.groups.set((user_group.first(),))
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('email', '')
        extra_fields.setdefault('first_name', '')
        extra_fields.setdefault('last_name', '')
        extra_fields.setdefault('birth_date', now().date())
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)
