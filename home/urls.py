from django.urls import path
from .views import home_view, loading_view

urlpatterns = [
    path('', home_view, name='home'),
    path("loading/", loading_view, name="loading"),
]
