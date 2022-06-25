from django.db import models

from core.models import AbstractModel
from game.models import Genre, Platform, Rating


class Game(AbstractModel):
    name = models.CharField(max_length=128)
    cover = models.URLField(null=True)
    storyline = models.CharField(max_length=256, null=True)
    description = models.TextField(max_length=2048, null=True)
    date_release = models.DateField(null=True)

    rating = models.ForeignKey(
        to=Rating,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    genres = models.ManyToManyField(
        to=Genre
    )
    platforms = models.ManyToManyField(
        to=Platform
    )

    def __str__(self):
        return self.name
