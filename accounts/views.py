from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import Account
import random
from django.contrib.auth import authenticate, login, logout

def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user object but don't save yet
            user = form.save(commit=False)

            # Generate unique username from email
            base_username = user.email.split('@')[0]
            username = base_username
            while Account.object.filter(username=username).exists():
                username = f"{base_username}{random.randint(1000, 9999)}"
            user.username = username

            # Hash the password
            user.set_password(form.cleaned_data['password'])

            # Save user
            user.save()

            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email = email, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()
        
    context = {'form' : form}
    return render(request, 'accounts/login.html', context)
