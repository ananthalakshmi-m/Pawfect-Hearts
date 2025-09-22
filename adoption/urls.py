from django.urls import path
from . import views

urlpatterns = [
    path('', views.adoption_list, name='adoption_list'),
    path('add/', views.add_dog, name='add_dog'),
    path('<int:pk>/', views.dog_detail, name='dog_detail'),

    # Favorites
    path('toggle-favorite/<int:dog_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_dogs, name='favorite_dogs'),

    # User's dogs
    path('manage/<int:pk>/', views.manage_dog, name='manage_dog'),

    # Edit/Delete/Adopt actions
    path('edit/<int:pk>/', views.edit_dog, name='edit_dog'),
    path('delete/<int:pk>/', views.delete_dog, name='delete_dog'),
    path('<int:pk>/confirm-adopted/', views.confirm_mark_adopted, name='confirm_mark_adopted'),
]
