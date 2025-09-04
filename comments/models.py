from django.db import models
from blog.models import Post
from accounts.models import Account

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"