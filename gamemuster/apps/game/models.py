from django.db import models

from core.models import AbstractModel
from user.models import CustomUser


class Genre(AbstractModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}, {self.name}, {self.created_at}>'


class Screenshot(AbstractModel):
    url = models.URLField(unique=True)

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}, {self.url}, {self.created_at}>'


class Platform(AbstractModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}, {self.name}, {self.created_at}>'


class Rating(AbstractModel):
    users = models.FloatField(null=True)
    users_count = models.IntegerField(null=True)
    critics = models.FloatField(null=True)
    critics_count = models.IntegerField(null=True)
    total = models.FloatField(null=True)
    total_count = models.IntegerField(null=True)


class Game(AbstractModel):
    name = models.CharField(max_length=128)
    logo = models.URLField()
    storyline = models.CharField(max_length=256, null=True)
    description = models.TextField(max_length=2048, null=True)
    date_release = models.CharField(default='', max_length=64, null=True)

    rating = models.ForeignKey(to=Rating, null=True, on_delete=models.CASCADE)
    genres = models.ManyToManyField(to=Genre)
    platforms = models.ManyToManyField(to=Platform)
    screenshots = models.ManyToManyField(to=Screenshot)

    def __str__(self):
        return self.name


class Musts(AbstractModel):
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='musts'
    )

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}, {self.game}, {self.user}, {self.created_at}>'

    class Meta:
        verbose_name = 'Musts'
        verbose_name_plural = 'Musts'
