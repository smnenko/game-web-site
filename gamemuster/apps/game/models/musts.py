from django.db import models

from core.models import AbstractModel
from game.models.game import Game
from user.models import CustomUser


class Musts(AbstractModel):
    game = models.ForeignKey(
        to=Game,
        on_delete=models.CASCADE,
        related_name='musts'
    )
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
