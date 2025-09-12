from django.shortcuts import redirect
from functools import wraps
# decorators for user access to different ways

def unauthenticated(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view(request, *args, **kwargs)
    return wrapper