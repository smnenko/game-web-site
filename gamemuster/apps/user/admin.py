from django.contrib import admin
from .models import CustomUser
from .models import Avatar


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'birth_date', 'avatar']
    list_display_links = ['username']


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id', 'avatar']
    list_display_links = ['avatar']
