from django.contrib import admin
from .models import CustomUser
from .models import Avatar


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'avatar']


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['avatar', 'pk']
