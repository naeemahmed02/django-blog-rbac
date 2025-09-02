from django.contrib import admin
from .models import Comments

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'updated_at', 'approved']
    list_editable = ['approved']