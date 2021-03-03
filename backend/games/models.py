from django.db import models
from datetime import datetime

# Create your models here.


class AbstractModel(models.Model):
    id = models.IntegerField(primary_key=True)
    date_created = models.DateTimeField(default=datetime.now)


class Genre(AbstractModel):
    name = models.CharField(max_length=32)


class Platform(AbstractModel):
    name = models.CharField(max_length=32)


class Rating(AbstractModel):
    users = models.IntegerField()
    users_reviews = models.IntegerField()
    critics = models.IntegerField()
    critics_reviews = models.IntegerField()


class Game(AbstractModel):
    name = models.CharField(max_length=128)
    short_description = models.CharField(max_length=256)
    logo = models.URLField()
    description = models.TextField(max_length=2048)
    categories = models.ManyToManyField(to=Genre)
    date_release = models.DateTimeField(default=datetime.now)
    ratings = models.ForeignKey(to=Rating, on_delete=models.CASCADE)


class Screenshot(AbstractModel):
    game_id = models.ForeignKey(to=Game, on_delete=models.CASCADE)
