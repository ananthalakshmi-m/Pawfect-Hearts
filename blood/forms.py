from django import forms
from .models import Donor, BloodRequest

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'dog_name', 'breed', 'age', 'blood_type',
            'available', 'contact_info', 'location', 'email', 'health_certificate'
        ]
        widgets = {
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_health_certificate(self):
        file = self.cleaned_data.get('health_certificate')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size should not exceed 5MB.")
        return file


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'dog_name', 'breed', 'age', 'blood_type_needed',
            'reason', 'contact_info', 'location', 'urgency_level'
        ]
        widgets = {
            'blood_type_needed': forms.Select(attrs={'class': 'form-select'}),
            'urgency_level': forms.Select(attrs={'class': 'form-select'}),
        }
