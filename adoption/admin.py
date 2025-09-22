from django.contrib import admin
from .models import Dog

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'breed', 'location', 'is_adopted')
    list_filter = ('is_adopted', 'breed', 'location')
    search_fields = ('name', 'breed', 'location')