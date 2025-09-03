from django.urls import path
from . import views

urlpatterns = [
    path('<str:post_category>/<slug:post_slug>/', views.single_post, name='single_post'),
]
