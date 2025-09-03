from django.shortcuts import render, get_object_or_404
from .models import Post

def single_post(request, post_category:str, post_slug:str):
    post = get_object_or_404(
        Post,
        category__slug = post_category,
        slug = post_slug
    )
    return render(request, 'blog/single_post.html', {'post': post})
