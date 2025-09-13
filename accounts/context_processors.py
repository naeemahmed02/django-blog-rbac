from .models import Account
from django.shortcuts import get_object_or_404

def user_profile(request):
    if request.user.is_authenticated:
        try:
            user = get_object_or_404(Account, username = request.user.username)
            return {'user_profile': user}
        except Account.DoesNotExist:
            return {'user_profile': None}

    return {'user_profile': None}