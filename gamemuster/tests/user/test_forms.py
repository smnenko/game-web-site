from django.test import TestCase
from django.utils import timezone

from user.forms import SignUpForm


class SignUpFormTestCase(TestCase):
    def test__form_valid(self):
        form_data = {
            'username': 'custom_user',
            'email': 'custom.mail@gmail.com',
            'first_name': 'custom_name',
            'last_name': 'custom_surname',
            'birth_date': timezone.now().date(),
            'password': 'Qwerty12345',
            'password_confirm': 'Qwerty12345',
        }
        form = SignUpForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password'], form.cleaned_data['password_confirm'])

    def test__form_invalid_email(self):
        form_data = {
            'username': 'custom_user',
            'email': 'custom.mail',
            'first_name': 'custom_name',
            'last_name': 'custom_surname',
            'birth_date': timezone.now().date(),
            'password': 'Qwerty12345',
            'password_confirm': 'Qwerty12345',
        }
        form = SignUpForm(form_data)
        self.assertFalse(form.is_valid())

    def test__form_invalid_password(self):
        form_data = {
            'username': 'custom_user',
            'email': 'custom.mail@gmail.com',
            'first_name': 'custom_name',
            'last_name': 'custom_surname',
            'birth_date': timezone.now().date(),
            'password': 'Qwerty12345',
            'password_confirm': 'Qwerty1234',
        }
        form = SignUpForm(form_data)
        self.assertFalse(form.is_valid())
