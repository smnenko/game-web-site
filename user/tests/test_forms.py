from django.test import TestCase
from django.utils import timezone

from user.forms import SignUpForm


class SignUpFormTestCase(TestCase):
    def test_form(self):
        form_data = {
            'username': 'custom_user',
            'email': 'custom.mail@gmail.com',
            'first_name': 'custom_name',
            'last_name': 'custom_surname',
            'birth_date': timezone.now().date(),
            'password': 'Qwerty12345',
            'confirm_password': 'Qwerty12345',
        }
        form = SignUpForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password'], form.cleaned_data['confirm_password'])
