import factory
import faker


faker = faker.Faker('en_US')


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'games.Genre'
        django_get_or_create = ('name', )
    name = 'Indie'


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'games.Platform'
        django_get_or_create = ('name', )
    name = 'Windows'


class ScreenshotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'games.Screenshot'
        django_get_or_create = ('url',)
    url = 'https://google.com/'


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'games.Game'
        django_get_or_create = ('name', 'short_description')
    name = faker.name()
    short_description = 'It is a platform game developed and published by Nintendo.'
