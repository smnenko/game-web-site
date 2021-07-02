from django.test import TestCase
from django.utils import timezone

from user.models import CustomUser


class LoginFormViewTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(
            username='custom',
            password='custompasswd',
            email='custom@gmail.com',
            first_name='Custom',
            last_name='User',
            birth_date=timezone.now().date()
        )

    def test_login_exists(self):
        resp = self.client.get('/login')
        self.assertTrue(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/login.html')

    def test_login_success(self):
        user_login = self.client.login(username='custom', password='custompasswd')
        self.assertTrue(user_login)

    def test_redirects(self):
        resp = self.client.get('/profile')
        self.assertRedirects(resp, '/login?next=/profile')


class SignupFormViewTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(
            username='custom1',
            password='custompasswd',
            email='custom1@gmail.com',
            first_name='Custom',
            last_name='User',
            birth_date=timezone.now().date()
        )

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


class ProfileListViewTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(
            username='custom',
            password='custompasswd',
            email='custom@gmail.com',
            first_name='Custom',
            last_name='User',
            birth_date=timezone.now().date()
        )

    def test_profile_exists(self):
        user_login = self.client.login(username='custom', password='custompasswd')
        self.assertTrue(user_login)
        resp = self.client.get('/profile')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/profile.html')
