from django.shortcuts import redirect
# decorators for user access to different ways

def unauthenticated(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request)
        else:
            return redirect('user_login')
    return wrapper()