from django.contrib import admin

from game.models import Game
from game.models import Musts
from game.models import Genre
from game.models import Platform
from game.models import Screenshot
from game.models import Rating


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_genres', 'get_platforms', 'cover', 'created_at']
    list_display_links = ['name']
    list_filter = ['genres', 'platforms']

    def get_genres(self, obj):
        return ', '.join(genre.name for genre in obj.genres.all())

    def get_platforms(self, obj):
        return ', '.join(platform.name for platform in obj.platforms.all())


@admin.register(Musts)
class MustsAdmin(admin.ModelAdmin):
    list_display = ['id', 'game', 'user']
    list_display_links = ['game']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['name']


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['name']


@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ['id', 'game', 'url', 'created_at']
    list_display_links = ['game']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
