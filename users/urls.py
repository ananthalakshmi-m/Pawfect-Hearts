from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup

urlpatterns = [
    path("signup/", signup, name="signup"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login"
    ),
]
