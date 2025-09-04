from django.shortcuts import render, get_object_or_404
from .models import Post
from comments.forms import CommentForm
from comments.models import Comments

def single_post(request, post_category:str, post_slug:str):
    post = get_object_or_404(
        Post,
        category__slug = post_category,
        slug = post_slug
    )
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comments.objects.create(
                
            )
    else:
        form = CommentForm()
    return render(request, 'blog/single_post.html', {'post': post, 'form': form})
