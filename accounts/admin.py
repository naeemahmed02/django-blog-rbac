from django.contrib import admin
from .models import Account, Profile
from django.contrib.auth.admin import UserAdmin

@admin.register(Account)
class CategoryAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'phone_number', 'date_joined', 'last_login', 'is_active')
    readonly_fields = ('date_joined', 'last_login')
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ['profile_pic']