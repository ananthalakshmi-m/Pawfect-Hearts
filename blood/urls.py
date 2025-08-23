from django.urls import path
from . import views

urlpatterns = [
    path('donors/', views.donor_list, name='donor_list'),
    path('donors/<int:pk>/', views.donor_detail, name='donor_detail'),

    # Add/Register
    path('register/', views.register_donor, name='register_donor'),

    # Manage current user's donor profile
    path('manage/<int:pk>/', views.manage_donor, name='manage_donor'),

    # Toggle availability
    path('donors/<int:pk>/toggle-availability/', views.toggle_donor_availability, name='toggle_donor_availability'),

    # Edit/Delete donor
    path('edit/<int:pk>/', views.edit_donor, name='edit_donor'),
    path('delete/<int:pk>/', views.delete_donor, name='delete_donor'),

    # Blood request
    path('request/', views.request_blood, name='request_blood'),
    path('requests/', views.blood_requests, name='blood_requests'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/manage/<int:pk>/', views.manage_request, name='manage_request'),
    path('requests/<int:pk>/confirm-fulfill/', views.confirm_fulfill_request, name='confirm_fulfill_request'),
    path('requests/<int:pk>/fulfill/', views.fulfill_request, name='mark_request_fulfilled'),
    path('requests/<int:pk>/delete/', views.delete_request, name='delete_request'),
]
