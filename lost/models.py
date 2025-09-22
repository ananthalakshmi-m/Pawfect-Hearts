from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
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

class LostDog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, choices=BREED_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    last_seen_location = models.CharField(max_length=255)
    date_lost = models.DateField()
    contact_info = models.CharField(max_length=100, blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    found = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Found" if self.found else "Still Missing"
        return f"{self.name} (Lost by {self.owner.username}) - {status}"

    class Meta:
        ordering = ['-date_lost']
        verbose_name = "Lost Dog"
        verbose_name_plural = "Lost Dogs"


class FoundDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, choices=BREED_CHOICES, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True)
    found_location = models.CharField(max_length=255)
    found_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    found_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    date_found = models.DateField()
    image = CloudinaryField('image')
    matched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        breed_display = self.breed if self.breed else "Unknown Breed"
        status = "Matched" if self.matched else "Unmatched"
        return f"Found Dog ({breed_display}) - {status}"

    class Meta:
        ordering = ['-date_found']
        verbose_name = "Found Dog"
        verbose_name_plural = "Found Dogs"
