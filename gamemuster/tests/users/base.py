from django.test import TestCase

from gamemuster.tests.users.factories import UserFactory


class BaseUserTestCase(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory.create()
        self.user.set_password('12345678')
        self.user.save()
