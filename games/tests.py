import factory
import pytest
from django.test import TestCase

from games.models import Game
from games.models import Genre
from games.models import Platform
from games.models import Screenshot


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'games.Genre'
        django_get_or_create = ('name', )
    name = 'Indie'


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'games.Platform'
        django_get_or_create = ('name',)
    name = 'Windows'


class ScreenshotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'games.Screenshot'
        django_get_or_create = ('url',)
    url = 'https://google.com/'


class GenreTestCase(TestCase):
    def setUp(self):
        GenreFactory()

    def test_genres_if_exists(self):
        self.assertTrue(Genre.objects.filter(name='Indie').exists())


class PlatformTestCase(TestCase):
    def setUp(self):
        PlatformFactory()

    def test_platforms_if_exists(self):
        self.assertTrue(Platform.objects.filter(name='Windows').exists())


class ScreenshotTestCase(TestCase):
    def setUp(self):
        ScreenshotFactory()

    def test_screenshots_if_exists(self):
        self.assertTrue(Screenshot.objects.filter(url='https://google.com/').exists())
