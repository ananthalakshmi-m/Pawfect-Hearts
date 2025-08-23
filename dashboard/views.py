from django.shortcuts import render
from adoption.models import Dog
from blood.models import Donor, BloodRequest
from lost.models import LostDog, FoundDog
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def user_dashboard(request):
    user = request.user

    dogs = Dog.objects.filter(added_by=user)
    donors = Donor.objects.filter(user=user)
    blood_requests = BloodRequest.objects.filter(user=user)
    lost_dogs = LostDog.objects.filter(owner=user)
    found_dogs = FoundDog.objects.filter(user=user)

    if not (dogs.exists() or donors.exists() or blood_requests.exists() or lost_dogs.exists() or found_dogs.exists()):
        messages.info(request, "Welcome! You haven't added anything yet. Start by exploring the features.")

    return render(request, 'dashboard/user_dashboard.html', {
        'dogs': dogs,
        'donors': donors,
        'blood_requests': blood_requests,
        'lost_dogs': lost_dogs,
        'found_dogs': found_dogs,
    })
