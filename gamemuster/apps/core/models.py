from django.db import models
from django.utils.timezone import now


class AbstractModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = now()
        return super().save(*args, **kwargs)
