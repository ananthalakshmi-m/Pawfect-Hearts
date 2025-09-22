from django import forms
from .models import Dog

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = [
            'name', 'age', 'breed', 'description', 'location',
            'contact_info', 'image', 'health_certificate',
            'gender', 'vaccinated', 'sterilized', 'temperament', 'medical_notes'
        ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/png,image/jpeg,image/jpg'}),
            'health_certificate': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }

    def clean_health_certificate(self):
        file = self.cleaned_data.get('health_certificate')
        if file and hasattr(file, 'content_type'):
            if file.content_type != 'application/pdf':
                raise forms.ValidationError("Only PDF files are allowed for the health certificate.")
        return file
