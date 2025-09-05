from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from comments.forms import CommentForm
from comments.models import Comments
from django.core.paginator import Paginator


def single_post(request, post_category:str, post_slug:str):
    current_user = request.user
    post = get_object_or_404(
        Post,
        category__slug = post_category,
        slug = post_slug
    )
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            Comments.objects.create(
                post = post,
                author = current_user,
                message = message,
            )
            return redirect(request.path)
    else:
        form = CommentForm()
    comments = Comments.objects.filter(post = post)
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/single_post.html', context)


def articles(request):
    articles = Post.objects.filter(status = 'published')
    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'articles': articles, 'page_obj': page_obj}
    return render(request, 'blog/articles.html', context)