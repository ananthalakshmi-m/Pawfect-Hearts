from django import forms
from .models import LostDog, FoundDog

class LostDogForm(forms.ModelForm):
    class Meta:
        model = LostDog
        fields = [
            'name', 'breed', 'gender', 'age', 'description',
            'last_seen_location', 'date_lost', 'contact_info', 'image'
        ]
        widgets = {
            'date_lost': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }


class FoundDogForm(forms.ModelForm):
    class Meta:
        model = FoundDog
        fields = [
            'contact_info', 'breed', 'gender',
            'description', 'found_location', 'date_found', 'image'
        ]
        widgets = {
            'date_found': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }

