from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField

BLOOD_TYPE_CHOICES = [
    ('DEA 1.1+', 'DEA 1.1 Positive'),
    ('DEA 1.1-', 'DEA 1.1 Negative'),
    ('DEA 1.2', 'DEA 1.2'),
    ('DEA 3', 'DEA 3'),
    ('DEA 4', 'DEA 4'),
    ('DEA 5', 'DEA 5'),
    ('DEA 7', 'DEA 7'),
]

BREED_CHOICES = [
    ('Beagle', 'Beagle'),
    ('Border Collie', 'Border Collie'),
    ('Boxer', 'Boxer'),
    ('Bulldog', 'Bulldog'),
    ('Chihuahua', 'Chihuahua'),
    ('Cocker Spaniel', 'Cocker Spaniel'),
    ('Dalmatian', 'Dalmatian'),
    ('Dachshund', 'Dachshund'),
    ('Doberman Pinscher', 'Doberman Pinscher'),
    ('German Shepherd', 'German Shepherd'),
    ('Golden Retriever', 'Golden Retriever'),
    ('Great Dane', 'Great Dane'),
    ('Labrador Retriever', 'Labrador Retriever'),
    ('Pomeranian', 'Pomeranian'),
    ('Poodle', 'Poodle'),
    ('Pug', 'Pug'),
    ('Rottweiler', 'Rottweiler'),
    ('Siberian Husky', 'Siberian Husky'),
    ('Shih Tzu', 'Shih Tzu'),
    ('Other', 'Other'),
]

URGENCY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
]

class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog_name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, choices = BREED_CHOICES)
    age = models.PositiveIntegerField()
    blood_type = models.CharField(max_length=10, choices=BLOOD_TYPE_CHOICES)
    contact_info = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    health_certificate = CloudinaryField(
        'health_certificate',
        resource_type='raw',
        folder='health_certificates',
        use_filename=True,
        unique_filename=False,
        overwrite=True
    )

    def __str__(self):
        return f"{self.dog_name} ({self.blood_type})"

class BloodRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog_name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, choices = BREED_CHOICES)
    age = models.PositiveIntegerField()
    blood_type_needed = models.CharField(max_length=10, choices=BLOOD_TYPE_CHOICES)
    reason = models.TextField()
    contact_info = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    is_fulfilled = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dog_name} - {self.blood_type_needed}"

    def get_absolute_url(self):
        return reverse('request_detail', kwargs={'pk': self.pk})
    