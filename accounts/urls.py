from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import StyledPasswordResetForm, StyledSetPasswordForm

urlpatterns = [
    path("register/", views.user_registration, name="user_registration"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="logout"),
    path('@<str:username>', views.user_profile, name= "user_profile"),
    path('edit-profile/@<str:username>/', views.edit_user_profile, name= "edit_user_profile"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    

    # Password reset (Django built-in)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="registration/password_reset_email.html",
            form_class = StyledPasswordResetForm
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            form_class = StyledSetPasswordForm
        ),
        
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    
]
