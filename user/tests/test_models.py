from django.test import TestCase
from django.utils import timezone

from user.tests.factories import CustomUserFactory, GroupFactory
from user.models import CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self):
        user = CustomUserFactory.create(groups=(GroupFactory.create(),))
        user.set_password('custompasswd')
        user.save()

    def test_user_exists(self):
        user = CustomUser.objects.filter(username='custom')
        self.assertTrue(user.exists())

    def test_user_fields(self):
        user = CustomUser.objects.filter(username='custom').first()
        username_max_length = user._meta.get_field('username').max_length
        first_name_max_length = user._meta.get_field('first_name').max_length
        last_name_max_length = user._meta.get_field('last_name').max_length
        self.assertEqual(username_max_length, 16)
        self.assertEqual(first_name_max_length, 64)
        self.assertEqual(last_name_max_length, 64)
        self.assertEqual(user.date_joined, timezone.now().date())
