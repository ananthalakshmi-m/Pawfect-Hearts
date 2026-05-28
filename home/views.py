import json
from django.shortcuts import render
from adoption.models import Dog
from lost.models import LostDog, FoundDog
from blood.models import BloodRequest
from notifications_pane.models import Notification

def home_view(request):
    recent_dogs = Dog.objects.filter(is_adopted=False).order_by('-date_added')[:8]
    recent_lost_dogs = LostDog.objects.order_by('-created_at')[:8]
    recent_found_dogs = FoundDog.objects.filter(matched=False).order_by('-created_at')[:8]
    recent_blood_requests = BloodRequest.objects.order_by('-date_requested')[:8]
    recent_notifications = Notification.objects.order_by('-timestamp')[:8]

    # Convert DecimalFields to float for JSON
    found_dogs_data = []
    for dog in recent_found_dogs:
        if dog.found_latitude is not None and dog.found_longitude is not None:
            found_dogs_data.append({
                'id': dog.id,
                'lat': float(dog.found_latitude),
                'lng': float(dog.found_longitude),
                'image': dog.image.url if dog.image else None,
                'location': dog.found_location or "Unknown",
            })

    def chunked(iterable, size):
        return [iterable[i:i + size] for i in range(0, len(iterable), size)]

    context = {
        'dogs': recent_dogs,
        'grouped_lost_dogs': chunked(list(recent_lost_dogs), 4),
        'grouped_found_dogs': chunked(list(recent_found_dogs), 4),
        'grouped_blood_requests': chunked(list(recent_blood_requests), 4),
        'grouped_notifications': chunked(list(recent_notifications), 4),
        'found_dogs_data_json': json.dumps(found_dogs_data),
    }

    return render(request, 'home/home.html', context)
