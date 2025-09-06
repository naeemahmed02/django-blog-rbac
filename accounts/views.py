from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import Account
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


def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user object but don't save yet
            user = form.save(commit=False)

            # Generate unique username from email
            base_username = user.email.split("@")[0]
            username = base_username
            while Account.objects.filter(username=username).exists():
                username = f"{base_username}{random.randint(1000, 9999)}"
            user.username = username

            # Hash the password
            user.set_password(form.cleaned_data["password"])

            # Save user
            user.save()
            
            # send activation email
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )
            
            subject = "Activate Your Account"
            message = render_to_string("accounts/activation_email.html", {
                'user' : user,
                'activation_link' : activation_link,
                'year' : datetime.now().year
            })
            # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.content_subtype = "html"  # ✅ Important: send as HTML
            email.send()
            

            messages.success(
                request, "Account created! Please check your email to verify before logging in."
            )
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/registration.html", {"form": form})


# Activation View
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect("user_login")
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect("home")



def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)


def user_logout(request):
    logout(request)
    return redirect('home')
