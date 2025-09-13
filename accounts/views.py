from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, EditUserProfile
from .models import Account, Profile
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from blog.models import Post
from django.db.models import Sum
from . decorators import unauthenticated
from django.contrib.auth.decorators import login_required


# View to handle user registration
@unauthenticated
def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        # Validate form input
        if form.is_valid():
            # Create user object from form without saving it yet
            user = form.save(commit=False)

            # Generate a unique username based on the email prefix
            base_username = user.email.split("@")[0]
            username = base_username

            # Ensure the username is unique by appending random numbers if needed
            while Account.objects.filter(username=username).exists():
                username = f"{base_username}{random.randint(1000, 9999)}"
            user.username = username

            # Hash the raw password using Django’s set_password method
            user.set_password(form.cleaned_data["password"])

            # Save the user to the database
            user.save()

            # Prepare account activation email
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encode user ID
            token = default_token_generator.make_token(user)    # Generate token

            # Construct activation URL with encoded user ID and token
            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )

            # Email subject and body content
            subject = "Activate Your Account"
            message = render_to_string("accounts/activation_email.html", {
                'user': user,
                'activation_link': activation_link,
                'year': datetime.now().year
            })

            # Send the email in HTML format
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.content_subtype = "html"
            email.send()

            # Inform the user to check email for activation link
            messages.success(
                request, "Account created! Please check your email to verify before logging in."
            )
            return redirect("user_login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # If not POST, initialize an empty registration form
        form = UserRegistrationForm()

    return render(request, "accounts/registration.html", {"form": form})


# View to handle account activation from email link
def activate(request, uidb64, token):
    try:
        # Decode the base64 encoded user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # Check if the user and token are valid
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect("user_login")
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect("home")


# View to handle user login
@unauthenticated
def user_login(request):
    next_url = request.GET.get('next')  # For redirecting after login

    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Authenticate using email and password
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect(next_url or "home")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()

    # Include the next URL in the context for redirection after login
    context = {"form": form, next: next_url}
    return render(request, "accounts/login.html", context)

# View to display user profile
@login_required(login_url="user_login")
def user_profile(request, username):
    user = Account.objects.get(username=username)

    # If the current user is viewing their own profile
    if request.user == user:
        # Show all posts including drafts
        posts_by_user = Post.objects.filter(author=user)
    else:
        # Only show published posts to others
        posts_by_user = Post.objects.filter(author=user, status='published')

    # Get total views across all user's posts
    total_post_views = Post.objects.filter(author=user).aggregate(total_views=Sum("views"))
    total_post_views = total_post_views['total_views']

    context = {
        'user': user,
        'posts_by_user': posts_by_user,
        'total_post_views': total_post_views
    }
    return render(request, 'accounts/user_profile.html', context)


# View to edit user profile information
@login_required(login_url="user_login")
def edit_user_profile(request, username):
    # Ensure the account and profile exist for the given username
    account = get_object_or_404(Account, username=username)
    profile = get_object_or_404(Profile, user=account)

    if request.method == "POST":
        form = EditUserProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditUserProfile(instance=profile)

    context = {
        'form': form,
        'user': profile,
    }
    return render(request, 'accounts/edit_user_profile.html', context)



# View to handle user logout
def user_logout(request):
    logout(request)
    return redirect('home')


