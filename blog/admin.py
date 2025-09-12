from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'featured_image', 'category', 'status', 'claps', 'views', 'created_at']
    list_editable = ['status']
    search_fields = ['title', 'author__first_name', 'author__last_name', 'category__category_name']
    
