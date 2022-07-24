from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import CustomUser
from user.models import Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_email_confirmed', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('username',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')})
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
