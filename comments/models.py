# from django.db import models
# # from blog.models import Post
# from accounts.models import Account

# class Comments(models.Model):
#     post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
#     author = models.ForeignKey(Account, on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_at = models.DateTimeField(auto_now=True)