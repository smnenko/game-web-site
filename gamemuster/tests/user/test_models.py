from django.utils import timezone

from gamemuster.tests.user.base import BaseUserTestCase


class CustomUserTestCase(BaseUserTestCase):

    def test__user_necessary_fields_exists(self):
        user_fields = [i.name for i in self.user._meta.fields]

        self.assertIn('username', user_fields)
        self.assertIn('first_name', user_fields)
        self.assertIn('last_name', user_fields)
        self.assertIn('birth_date', user_fields)
        self.assertIn('password', user_fields)
        self.assertIn('last_login', user_fields)
        self.assertIn('is_active', user_fields)
        self.assertIn('is_staff', user_fields)
        self.assertIn('is_superuser', user_fields)
        self.assertIn('created_at', user_fields)
        self.assertIn('updated_at', user_fields)

    def test__user_fields_length(self):
        username_max_length = self.user._meta.get_field('username').max_length
        first_name_max_length = self.user._meta.get_field('first_name').max_length
        last_name_max_length = self.user._meta.get_field('last_name').max_length

        self.assertEqual(username_max_length, 16)
        self.assertEqual(first_name_max_length, 64)
        self.assertEqual(last_name_max_length, 64)
        self.assertEqual(self.user.created_at.date(), timezone.now().date())

    def test__user_default_group(self):
        self.assertIn(self.user_group, self.user.groups.all())
