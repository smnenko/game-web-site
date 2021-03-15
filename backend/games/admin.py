from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'genres', 'platforms', 'ratings_users', 'ratings_critics']
    list_filter = ['genres', 'platforms']