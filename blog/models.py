from django.db import models
from category.models import Category
from comments.models import Comments

STATUS = (
    ('draft', 'Draft'),
    ('published', 'Published')
)

class POST(models.Model):
    title = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=1200, unique=True, blank=True)
    # author = ''
    content = models.TextField()
    featured_image = models.ImageField(upload_to='media/post_featured_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    claps = models.IntegerField(default=0)
    status = models.CharField(choices=STATUS, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    