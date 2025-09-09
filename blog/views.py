from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from comments.forms import CommentForm
from comments.models import Comments
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import GuestPostForm
from django.contrib.auth.decorators import login_required
from category.models import Category
from django.contrib import messages
import time
import random


def single_post(request, post_category: str, post_slug: str):
    current_user = request.user
    post = get_object_or_404(Post, category__slug=post_category, slug=post_slug)
    # count views on the post

    # Build a session key specific to the post
    session_key = f"viewed_post{post.id}"
    print(session_key)
    now = time.time()  # seconds

    # How long before we allow counting again (30 minutes = 1800 seconds)
    cooldown = 30 * 60

    last_viewed = request.session.get(session_key)

    if not last_viewed or (now - last_viewed) > cooldown:
        # Increment views only if not seen in last 30 minutes
        post.views += 1
        post.save(update_fields=["views"])
        request.session[session_key] = now

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
            return redirect("guest_posts")
    else:
        form = GuestPostForm()
    context = {"form": form}
    return render(request, "blog/guest_post.html", context)


@login_required(login_url="user_login")
def guest_posts(request):
    query = request.GET.get("query")
    if query:
        user_posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-created_at")
    else:
        user_posts = Post.objects.filter(author=request.user).order_by("-created_at")
    context = {"user_posts": user_posts}
    return render(request, "blog/guest_posts.html", context)


@login_required(login_url="user_login")
def edit_guest_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == "POST":
        form = GuestPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Your post has been updated successfully.")
            return redirect("guest_posts")

    else:
        form = GuestPostForm(instance=post)
    context = {"form": form}
    return render(request, "blog/edit_guest_post.html", context)


@login_required(login_url="user_login")
def delete_guest_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    post.delete()
    return redirect("guest_posts")
