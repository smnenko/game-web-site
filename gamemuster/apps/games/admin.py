from django.contrib import admin

from games.models import Game
from games.models import Musts
from games.models import Genre
from games.models import Platform
from games.models import Screenshot


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_genres', 'get_platforms', 'ratings_users', 'ratings_critics']
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
    list_display = ['id', 'url', 'created_at']
    list_display_links = ['url']
