from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone

from gamemuster.tests.user.factories import CustomUserFactory


class BaseUserTestCase(TestCase):

    def setUp(self) -> None:
        self.username = 'custom_user'
        self.password = '12345678'
        self.user_group = Group.objects.create(name='Users')
        self.permissions = [
            Permission.objects.get(name='Can view game'),
            Permission.objects.get(name='Can add Musts'),
            Permission.objects.get(name='Can view Musts'),
            Permission.objects.get(name='Can change Musts'),
            Permission.objects.get(name='Can delete Musts'),
        ]
        self.user_group.permissions.set(self.permissions)
        self.user = CustomUserFactory.create(
            username=self.username,
            groups=[self.user_group]
        )
        self.user.groups.set((self.user_group,))
        self.user.set_password('12345678')
        self.user.save(update_fields=('password',))


class BaseUserAuthTestCase(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.signup_data = {
            'username': 'custom',
            'first_name': 'Custom',
            'last_name': 'User',
            'email': 'custom_email@gmail.com',
            'birth_date': timezone.now().date(),
            'password': '12345678',
            'password_confirm': '12345678'
        }
        self.login_url = reverse_lazy('login')
        self.singup_url = reverse_lazy('signup')
        self.logout_url = reverse_lazy('logout')
        self.profile_url = reverse_lazy('profile', kwargs={'pk': self.user.id})
