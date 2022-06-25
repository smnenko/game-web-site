from django.db import models

from core.models import AbstractModel


class Genre(AbstractModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.id}, {self.name}, {self.created_at}>'
