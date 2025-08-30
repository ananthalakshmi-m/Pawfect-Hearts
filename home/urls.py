from django.urls import path
from .views import home_view, loading_view

urlpatterns = [
    path('', loading_view, name='loading'),
    path('home/', home_view, name='home'),
]