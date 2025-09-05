from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Post
from .utils import unique_slug_generator


@receiver(pre_save, sender = Post)
def add_unique_slug(sender, instance, **kwargs):
    """Automatically generate unique slug befor saving the post"""
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)