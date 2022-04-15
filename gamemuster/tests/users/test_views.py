from django.test import TestCase
from django.utils import timezone

from gamemuster.tests.users.factories import CustomUserFactory, GroupFactory


class BaseFormViewTestCase(TestCase):
    def setUp(self):
        user = CustomUserFactory.create(groups=(GroupFactory.create(), ))
        user.set_password('custompasswd')
        user.save()


class LoginFormViewTestCase(BaseFormViewTestCase):

    def test_login_exists(self):
        resp = self.client.get('/login')
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/login.html')

    def test_login_success(self):
        user_login = self.client.login(
            username='custom',
            password='custompasswd'
        )
        self.assertTrue(user_login)

    def test_redirects(self):
        resp = self.client.get('/profile')
        self.assertRedirects(resp, '/login?next=/profile')


class SignupFormViewTestCase(BaseFormViewTestCase):

    def test_signup_exists(self):
        resp = self.client.get('/signup')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/signup.html')

    def test_signup_success(self):
        data = {
            'username': 'custom',
            'first_name': 'Custom',
            'last_name': 'User',
            'birth_date': timezone.now().date(),
            'password': 'custompasswd'
        }
        resp = self.client.get('/signup', data, follow=True)
        self.assertEqual(resp.status_code, 200)


class ProfileListViewTestCase(BaseFormViewTestCase):

    def test_profile_exists(self):
        user_login = self.client.login(username='custom', password='custompasswd')
        self.assertTrue(user_login)
        resp = self.client.get('/profile')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/profile.html')
