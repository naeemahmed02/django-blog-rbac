from django.db import models

class Comments(models.Model):
    # user = 
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)