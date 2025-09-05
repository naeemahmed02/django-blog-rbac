import random
import string
from django.utils.text import slugify

def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    """
    Generates a random string of given size using lowercase letters and digits.
    Example: 'a9x2'
    """
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    Generates a unique slug for a given Django model instance.

    - Uses slugify on the instance's title (or "untitled" if empty).
    - Ensures slug length does not exceed the model's slug field max_length.
    - If a duplicate exists, appends a random 4-character string.
    - Keeps looping until a unique slug is found.
    """

    # Step 1: Base slug (from provided new_slug or instance.title)
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title or "untitled")  # fallback if title is empty

    # Step 2: Get model class and max_length of slug field
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length

    # Step 3: Trim slug if it exceeds max_length
    slug = slug[:max_length]

    # Step 4: Loop until we find a unique slug
    while Klass.objects.filter(slug=slug).exists():
        # Append a random string (truncate base slug to make space)
        slug = "{slug}-{randstr}".format(
            slug=slug[:max_length-5],  # reserve space for "-xxxx"
            randstr=random_string_generator(size=4)
        )
        # Ensure slug fits into DB field
        slug = slug[:max_length]

    return slug
