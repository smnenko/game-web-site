from django.contrib import admin
from .models import Game, Musts


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'genres', 'platforms', 'ratings_users', 'ratings_critics']
    list_filter = ['genres', 'platforms']


@admin.register(Musts)
class MustsAdmin(admin.ModelAdmin):
    list_display = ['game', 'user']
