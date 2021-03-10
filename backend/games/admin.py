from django.contrib import admin
from .models import Game, Genre, Platform, Rating

# Register your models here.
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Rating)
