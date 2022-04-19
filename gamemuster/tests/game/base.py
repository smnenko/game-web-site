from django.test import TestCase
from django.urls import reverse_lazy

from gamemuster.tests.game.factories import (
    GenreFactory,
    PlatformFactory,
    ScreenshotFactory,
    GameFactory,
    MustFactory
)
from gamemuster.tests.user.base import BaseUserTestCase


class BaseGenreTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.genre = GenreFactory()


class BasePlatformTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.platform = PlatformFactory()


class BaseScreenshotTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.screenshot = ScreenshotFactory()


class BaseGameTestCase(
    BaseGenreTestCase,
    BasePlatformTestCase,
    BaseScreenshotTestCase
):
    def setUp(self):
        super().setUp()
        self.game = GameFactory(
            genres=[self.genre],
            platforms=[self.platform],
            screenshots=[self.screenshot]
        )


class BaseMustTestCase(BaseGameTestCase, BaseUserTestCase):
    def setUp(self):
        super().setUp()
        self.must = MustFactory(user=self.user, game=self.game)


class BaseGameViewTestCase(
    BaseMustTestCase,
    BaseGameTestCase,
    BaseUserTestCase
):
    def setUp(self):
        super().setUp()
        self.game_url = reverse_lazy('game', kwargs={'pk': self.game.id})
        self.games_url = reverse_lazy('games')
        self.musts_url = reverse_lazy('musts')
        self.login_url = reverse_lazy('login')
