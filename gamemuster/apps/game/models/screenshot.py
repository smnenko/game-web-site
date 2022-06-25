from django.db import models

from core.models import AbstractModel
from game.models import Game


class Screenshot(AbstractModel):
    game = models.ForeignKey(
        to=Game,
        null=True,
        on_delete=models.CASCADE,
        related_name='screenshots'
    )
    url = models.URLField(unique=True)

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}, {self.url}>'
