import factory


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'game.Genre'
        django_get_or_create = ('name',)

    name = 'Indie'


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'game.Platform'
        django_get_or_create = ('name',)

    name = 'Windows'


class ScreenshotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'game.Screenshot'
        django_get_or_create = ('url',)

    url = 'https://google.com/'


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'game.Game'
        django_get_or_create = ('name', 'storyline')

    name = 'Super Mario Bros.'
    storyline = 'It is a platformer developed and published by Nintendo.'

    @factory.post_generation
    def genres(self, created, extracted, **kwargs):
        if not created:
            return

        if extracted:
            self.genres.set(extracted)

    @factory.post_generation
    def platforms(self, created, extracted, **kwargs):
        if not created:
            return

        if extracted:
            self.platforms.set(extracted)

    @factory.post_generation
    def screenshots(self, created, extracted, **kwargs):
        if not created:
            return

        if extracted:
            self.screenshots.set(extracted)


class MustFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'game.Musts'
        django_get_or_create = ('user', 'game')
