from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup
from .forms import SendGridPasswordResetForm

urlpatterns = [
    path("signup/", signup, name="signup"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login"
    ),
    
     # Password reset URLs
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            form_class=SendGridPasswordResetForm,
            success_url="/users/password_reset_done/"
        ),
        name="password_reset"
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/users/password_reset_complete/"
        ),
        name="password_reset_confirm"
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]
