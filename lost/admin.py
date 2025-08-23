from django.contrib import admin
from .models import LostDog, FoundDog

admin.site.register(LostDog)
admin.site.register(FoundDog)