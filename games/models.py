from django.db import models

from user.models import CustomUser


class Game(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    short_description = models.CharField(max_length=128)
    logo = models.URLField()
    description = models.TextField(max_length=2048, null=True)
    genres = models.CharField(default='', max_length=128, null=True)
    platforms = models.CharField(default='', max_length=256, null=True)
    date_release = models.CharField(default='', max_length=64, null=True)
    screenshots = models.TextField(max_length=1024, null=True)
    ratings_users = models.CharField(default='', max_length=64, null=True)
    ratings_users_count = models.CharField(default='', max_length=64, null=True)
    ratings_critics = models.CharField(default='', max_length=64, null=True)
    ratings_critics_count = models.CharField(default='', max_length=64, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f'Game[{self.id}, {self.name}, {self.description[:32]}, {self.genres}, '
            f'{self.date_release}, {self.date_created}'
        )


class Musts(models.Model):
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Musts'
        verbose_name_plural = 'Musts'
