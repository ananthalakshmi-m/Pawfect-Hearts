from django.urls import path
from . import views

urlpatterns = [
    #Lost dogs
    path('', views.lost_dogs_list, name='lost_dogs_list'),
    path('report/', views.report_lost_dog, name='report_lost_dog'),
    path('lost/<int:pk>/', views.lost_dog_detail, name='lost_dog_detail'),
    path('lost/<int:pk>/edit/', views.edit_lost_dog, name='edit_lost_dog'),
    path('lost/<int:pk>/delete/', views.delete_lost_dog, name='delete_lost_dog'),
    path('lost/manage/<int:pk>/', views.manage_lost_dog, name='manage_lost_dog'),
    path('lost/<int:pk>/mark-found/', views.mark_lost_dog_found, name='mark_lost_dog_found'),

    #Found dogs
    path('found/', views.found_dogs_list, name='found_dogs_list'),
    path('found/report/', views.report_found_dog, name='report_found_dog'),
    path('found/<int:pk>/', views.found_dog_detail, name='found_dog_detail'),
    path('found/<int:pk>/edit/', views.edit_found_dog, name='edit_found_dog'),
    path('found/<int:pk>/delete/', views.delete_found_dog, name='delete_found_dog'),
    path('found/manage/<int:pk>/', views.manage_found_dog, name='manage_found_dog'),
    path('found/<int:pk>/mark-matched/', views.mark_found_dog_matched, name='mark_found_dog_matched'),
]
