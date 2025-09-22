from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Dog(models.Model):
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

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=100, choices=BREED_CHOICES)
    description = models.TextField()
    image = CloudinaryField('image')
    location = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=150)
    health_certificate = CloudinaryField(
        'health_certificate',
        resource_type='raw',
        folder='health_certificates',
        use_filename=True,
        unique_filename=False,
        overwrite=True
    )
    is_adopted = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dogs')
    date_added = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )
    vaccinated = models.BooleanField(default=False)
    sterilized = models.BooleanField(default=False)
    temperament = models.TextField()
    medical_notes = models.TextField(blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_dogs', blank=True)

    def __str__(self):
        return self.name