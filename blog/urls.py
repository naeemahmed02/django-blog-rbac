from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:post_category>/<slug:post_slug>/', views.single_post, name='single_post'),
    path('articles/', views.articles, name='articles'),
    path('add_guest_post/', views.add_guest_post, name='add_guest_post'),
]
