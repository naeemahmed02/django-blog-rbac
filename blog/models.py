from django.db import models
from category.models import Category
from accounts.models import Account



STATUS = (
    ('draft', 'Draft'),
    ('published', 'Published')
)

class Post(models.Model):
    title = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=1200, unique=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='post_featured_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    views = models.IntegerField(default=0)
    claps = models.IntegerField(default=0)
    status = models.CharField(choices=STATUS, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    


    
    