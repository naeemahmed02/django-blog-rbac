from django.shortcuts import render
from blog.models import Post
from category.models import Category


def home(request):
    hero_posts = Post.objects.filter(status="published")[:3]
    categories = Category.objects.all()
    # Showing at least one post from each category
    category_posts = []
    for category in categories:
        post = category.posts.filter(status="published").order_by("-created_at").first()
        if post:
            category_posts.append(post)
    # Split posts into 3 columns
    col_1 = category_posts[0::3]  # every 3rd starting at 0
    col_2 = category_posts[1::3]  # every 3rd starting at 1
    col_3 = category_posts[2::3]  # every 3rd starting at 2
    
    # Trending posts based on views
    trending_posts_sidebar = Post.objects.filter(status = 'published').order_by('-views')[:6]
    context = {
        "hero_posts": hero_posts,
        "category_posts": category_posts,
        "col_1": col_1,
        "col_2": col_2,
        "col_3": col_3,
        'trending_posts_sidebar' : trending_posts_sidebar
    }
    print(context)
    return render(request, "core/index.html", context)
