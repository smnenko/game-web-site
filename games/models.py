from django.db import models
from django.utils.timezone import now

from user.models import CustomUser


class AbstractModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    date_created = models.DateTimeField(default=now)

    class Meta:
        abstract = True


class Genre(AbstractModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.id}, {self.name}, {self.date_created}]'


class Screenshot(AbstractModel):
    url = models.URLField(unique=True)

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.id}, {self.url}, {self.date_created}]'


class Platform(AbstractModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.id}, {self.name}, {self.date_created}]'


class Game(AbstractModel):
    name = models.CharField(max_length=128)
    short_description = models.CharField(max_length=128)
    logo = models.URLField()
    description = models.TextField(max_length=2048, null=True)
    genres = models.ManyToManyField(to=Genre)
    platforms = models.ManyToManyField(to=Platform)
    screenshots = models.ManyToManyField(to=Screenshot)
    date_release = models.CharField(default='', max_length=64, null=True)
    ratings_users = models.CharField(default='', max_length=64, null=True)
    ratings_users_count = models.CharField(default='', max_length=64, null=True)
    ratings_critics = models.CharField(default='', max_length=64, null=True)
    ratings_critics_count = models.CharField(default='', max_length=64, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'{self.__class__.__name__}[{self.id}, {self.name}, {self.description[:32]}, {self.genres}, '
            f'{self.date_release}, {self.date_created}'
        )


class Musts(AbstractModel):
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.id}, {self.game}, {self.user}, {self.date_created}]'

    class Meta:
        verbose_name = 'Musts'
        verbose_name_plural = 'Musts'
