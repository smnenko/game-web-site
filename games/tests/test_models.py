from django.test import TestCase
from django.utils import timezone

from games.models import Game
from games.models import Genre
from games.models import Platform
from games.models import Screenshot
from games.models import Musts
from user.models import CustomUser
from games.tests.factories import GenreFactory
from games.tests.factories import PlatformFactory
from games.tests.factories import ScreenshotFactory
from games.tests.factories import GameFactory
from user.tests.factories import CustomUserFactory


class GenreTestCase(TestCase):
    def setUp(self):
        GenreFactory()

    def test_genres_exists(self):
        self.assertTrue(Genre.objects.filter(name='Indie').exists())

    def test_genre_fields(self):
        genre = Genre.objects.filter(name='Indie').first()
        self.assertEqual(genre.id, genre.pk)
        self.assertEqual(genre.name, 'Indie')
        self.assertEqual(genre.date_created.date(), timezone.now().date())

    def test_fields_length(self):
        genre = Genre.objects.filter(name='Indie').first()
        name_max_length = genre._meta.get_field('name').max_length
        self.assertEqual(name_max_length, 128)


class PlatformTestCase(TestCase):
    def setUp(self):
        PlatformFactory()

    def test_platforms_if_exists(self):
        self.assertTrue(Platform.objects.filter(name='Windows').exists())

    def test_platform_fields(self):
        platform = Platform.objects.filter(name='Windows').first()
        self.assertEqual(platform.id, platform.pk)
        self.assertEqual(platform.name, 'Windows')
        self.assertEqual(platform.date_created.date(), timezone.now().date())

    def test_fields_length(self):
        platform = Platform.objects.filter(name='Windows').first()
        name_max_length = platform._meta.get_field('name').max_length
        self.assertEqual(name_max_length, 128)


class ScreenshotTestCase(TestCase):
    def setUp(self):
        ScreenshotFactory()

    def test_screenshots_if_exists(self):
        self.assertTrue(Screenshot.objects.filter(url='https://google.com/').exists())

    def test_screenshot_fields(self):
        screenshot = Screenshot.objects.filter(url='https://google.com/').first()
        self.assertEqual(screenshot.id, screenshot.pk)
        self.assertEqual(screenshot.url, 'https://google.com/')
        self.assertEqual(screenshot.date_created.date(), timezone.now().date())


class GameTestCase(TestCase):
    def setUp(self):
        game = GameFactory(name='Super Mario Bros.')
        genre = GenreFactory()
        platform = PlatformFactory()
        screenshot = ScreenshotFactory()
        game.genres.set([genre.pk, ])
        game.platforms.set([platform.pk, ])
        game.screenshots.set([screenshot.pk, ])

    def test_game_if_exists(self):
        self.assertTrue(Game.objects.filter(name='Super Mario Bros.').exists())

    def test_game_fields(self):
        game = Game.objects.filter(name='Super Mario Bros.').first()
        self.assertEqual(game.id, game.pk)
        self.assertEqual(game.name, 'Super Mario Bros.')
        self.assertEqual(game.short_description, 'It is a platform game developed and published by Nintendo.')
        self.assertEqual(game.genres.first(), Genre.objects.first())
        self.assertEqual(game.platforms.first(), Platform.objects.first())
        self.assertEqual(game.screenshots.first(), Screenshot.objects.first())
        self.assertEqual(game.date_created.date(), timezone.now().date())

    def test_fields_length(self):
        game = Game.objects.filter(id=1).first()
        name_max_length = game._meta.get_field('name').max_length
        s_description_max_length = game._meta.get_field('short_description').max_length
        description_max_length = game._meta.get_field('description').max_length
        self.assertEqual(name_max_length, 128)
        self.assertEqual(s_description_max_length, 128)
        self.assertEqual(description_max_length, 2048)


class MustsTestCase(TestCase):
    def setUp(self):
        user = CustomUserFactory()
        game = GameFactory()
        Musts.objects.create(game=game, user=user)

    def test_must_exists(self):
        user = CustomUser.objects.filter(username='custom').first()
        game = Game.objects.all().first()
        self.assertTrue(Musts.objects.filter(user=user, game=game).exists())
