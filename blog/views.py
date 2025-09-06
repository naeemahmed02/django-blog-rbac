from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from comments.forms import CommentForm
from comments.models import Comments
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import GuestPostForm
from django.contrib.auth.decorators import login_required
from category.models import Category


def single_post(request, post_category: str, post_slug: str):
    current_user = request.user
    post = get_object_or_404(Post, category__slug=post_category, slug=post_slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            Comments.objects.create(
                post=post,
                author=current_user,
                message=message,
            )
            return redirect(request.path)
    else:
        form = CommentForm()
    comments = Comments.objects.filter(post=post)
    context = {"post": post, "form": form, "comments": comments}
    return render(request, "blog/single_post.html", context)


def articles(request):
    categories = Category.objects.all()[:5]
    query = request.GET.get("query")
    category_slug = request.GET.get("category", "all")

    # start with published posts
    articles = Post.objects.filter(status="published")

    # filter by category (if not "all")
    if category_slug != "all":
        articles = articles.filter(category__slug=category_slug)

    # filter by search query (if present)
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(articles, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "articles": articles,
        "page_obj": page_obj,
        "query": query,
        "categories": categories,
        "selected_category": category_slug,
    }
    return render(request, "blog/articles.html", context)



@login_required(login_url="user_login")
def add_guest_post(request):
    if request.method == "POST":
        form = GuestPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.status = "draft"
            post.author = request.user
            post.save()
    else:
        form = GuestPostForm()
    context = {"form": form}
    return render(request, "blog/guest_post.html", context)


def guest_posts(request):
    user_posts = Post.objects.filter(author = request.user)
    context = {'user_posts': user_posts}
    return render(request, 'blog/guest_posts.html', context)
