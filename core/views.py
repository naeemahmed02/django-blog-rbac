from django.shortcuts import render
from blog.models import Post
from category.models import Category


def home(request):
    posts = Post.objects.filter(status = 'published').order_by('-created_at')[:5]
    context = {'posts': posts}
    return render(request, "core/index.html", context)
