from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.


class AbstractModel(models.Model):
    id = models.IntegerField(primary_key=True)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Genre(AbstractModel):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Platform(AbstractModel):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Rating(AbstractModel):
    users = models.FloatField()
    users_reviews = models.IntegerField()
    critics = models.FloatField()
    critics_reviews = models.IntegerField()


class Game(AbstractModel):
    name = models.CharField(max_length=128)
    short_description = models.CharField(max_length=256)
    logo = models.URLField()
    description = models.TextField(max_length=2048)
    genres = models.CharField(default='', max_length=128)
    platforms = models.CharField(default='', max_length=256)
    date_release = models.DateField(default=date.today)
    ratings_users = models.CharField(default='', max_length=32)
    ratings_critics = models.CharField(default='', max_length=32)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Game[{self.id}, {self.name}, {self.description[:32]}, {self.genres}, {self.date_release}, ' \
               f'{self.date_created}'


class Screenshot(AbstractModel):
    game_id = models.ForeignKey(to=Game, on_delete=models.DO_NOTHING)
    url = models.URLField()

    def __str__(self):
        return self.url
