from django.contrib.auth.models import AnonymousUser

from user.models import CustomUser
from gamemuster.tests.user.base import BaseUserAuthTestCase


class LoginFormViewTestCase(BaseUserAuthTestCase):

    def test__login_page_exists(self):
        resp = self.client.get(self.login_url)

        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/login.html')

    def test__login_success(self):
        is_login_success = self.client.login(
            username=self.username,
            password=self.password
        )

        self.assertTrue(is_login_success)

    def test__login_failed_username_invalid(self):
        is_login_success = self.client.login(
            username=f'{self.username}1',
            password=self.password
        )

        self.assertFalse(is_login_success)

    def test__login_failed_password_invalid(self):
        is_login_success = self.client.login(
            username=self.username,
            password=f'{self.password}1'
        )

        self.assertFalse(is_login_success)

    def test_redirects(self):
        resp = self.client.get(self.profile_url)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'{self.login_url}?next={self.profile_url}')


class SignupFormViewTestCase(BaseUserAuthTestCase):

    def test_signup_page_exists(self):
        resp = self.client.get(self.singup_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/signup.html')

    def test_signup_success(self):
        resp = self.client.post(self.singup_url, self.signup_data)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.login_url)
        self.assertTrue(CustomUser.objects.get(username=self.signup_data['username']))

    def test_signup_success_dont_proceed_login(self):
        resp = self.client.post(self.singup_url, self.signup_data, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('user', resp.context)
        self.assertIsInstance(resp.context['user'], AnonymousUser)
        self.assertTemplateUsed(resp, 'user/login.html')

    def test_signup_form_validation_password_confirm(self):
        self.signup_data['password'] = self.signup_data['password'][::-1]
        resp = self.client.post(self.singup_url, self.signup_data)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('form', resp.context)
        self.assertIn('password_confirm', resp.context['form'].errors)
        self.assertTrue(resp.context['form'].errors['password_confirm'])


class ProfileViewTestCase(BaseUserAuthTestCase):

    def test__profile_exists(self):
        user_login = self.client.login(
            username=self.username,
            password=self.password
        )

        self.assertTrue(user_login)

        resp = self.client.get(self.profile_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/profile.html')
