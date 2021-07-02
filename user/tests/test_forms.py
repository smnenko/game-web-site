from django.test import TestCase

from user.forms import LoginForm


class LoginFormTestCase(TestCase):
    def test_form_fields(self):
        form = LoginForm()
        self.assertTrue(form.fields['username'].label in [None, 'username'])
