from django.db import models

from core.models import AbstractModel


class Rating(AbstractModel):
    users = models.FloatField(null=True)
    users_count = models.IntegerField(null=True)
    critics = models.FloatField(null=True)
    critics_count = models.IntegerField(null=True)
    total = models.FloatField(null=True)
    total_count = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.users} {self.critics} {self.total}'
