from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LostDog, FoundDog
from .forms import LostDogForm, FoundDogForm
from django.db.models import Q

# LOST DOGS

def lost_dogs_list(request):
    dogs = LostDog.objects.filter(found=False).order_by('-date_lost')
    return render(request, 'lost/lost_dogs_list.html', {'dogs': dogs})

@login_required
def report_lost_dog(request):
    if request.method == 'POST':
        form = LostDogForm(request.POST, request.FILES)
        if form.is_valid():
            lost_dog = form.save(commit=False)
            lost_dog.owner = request.user
            lost_dog.save()
            messages.success(request, "Lost dog reported.")
            return redirect('lost_dogs_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LostDogForm()
    return render(request, 'lost/report_lost_dog.html', {'form': form})

def lost_dog_detail(request, pk):
    dog = get_object_or_404(LostDog, pk=pk)
    return render(request, 'lost/lost_dog_detail.html', {'dog': dog})

@login_required
def manage_lost_dog(request, pk):
    dog = get_object_or_404(LostDog, pk=pk)
    if dog.owner != request.user:
        messages.error(request, "Not authorized to manage this report.")
        return redirect('lost_dogs_list')
    return render(request, 'lost/manage_lost_dog.html', {'dog': dog})

@login_required
def edit_lost_dog(request, pk):
    dog = get_object_or_404(LostDog, pk=pk)
    if dog.owner != request.user:
        messages.error(request, "Not authorized to edit this report.")
        return redirect('lost_dogs_list')
    if dog.found:
        messages.warning(request, "Cannot edit. Dog already marked as found.")
        return redirect('manage_lost_dog', pk=dog.pk)
    if request.method == 'POST':
        form = LostDogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, "Report updated.")
            return redirect('manage_lost_dog', pk=dog.pk)
        else:
            messages.error(request, "Update failed. Check for errors.")
    else:
        form = LostDogForm(instance=dog)
    return render(request, 'lost/edit_lost_dog.html', {'form': form, 'dog': dog})

@login_required
def delete_lost_dog(request, pk):
    dog = get_object_or_404(LostDog, pk=pk, owner=request.user)
    if request.method == 'POST':
        dog.delete()
        messages.success(request, "Lost dog entry deleted.")
        return redirect('user_dashboard')
    return render(request, 'lost/delete_lost_dog.html', {'dog': dog})

@login_required
def mark_lost_dog_found(request, pk):
    dog = get_object_or_404(LostDog, pk=pk)
    if request.user != dog.owner:
        messages.error(request, "Not authorized to mark this dog.")
        return redirect('lost_dog_detail', pk=dog.pk)
    if dog.found:
        messages.info(request, "Already marked as found.")
        return redirect('manage_lost_dog', pk=dog.pk)
    if request.method == 'POST':
        dog.found = True
        dog.save()
        messages.success(request, f"{dog.name} marked as found.")
        return redirect('manage_lost_dog', pk=dog.pk)
    return render(request, 'lost/confirm_mark_found.html', {'dog': dog})


# FOUND DOGS

def found_dogs_list(request):
    search_query = request.GET.get('search', '')
    breed_filter = request.GET.get('breed', '')
    dogs = FoundDog.objects.filter(matched=False)

    if search_query:
        dogs = dogs.filter(
            Q(description__icontains=search_query) |
            Q(found_location__icontains=search_query)
        )

    if breed_filter == "Unknown":
        dogs = dogs.filter(Q(breed__isnull=True) | Q(breed__exact=''))
    elif breed_filter:
        dogs = dogs.filter(breed__iexact=breed_filter)

    dogs = dogs.order_by('-date_found')

    breeds = list(
        FoundDog.objects
        .exclude(breed__isnull=True)
        .exclude(breed__exact='')
        .values_list('breed', flat=True)
        .distinct()
    )
    breeds.append("Unknown")

    return render(request, 'lost/found_dogs_list.html', {
        'dogs': dogs,
        'search_query': search_query,
        'breed_filter': breed_filter,
        'breeds': breeds,
    })

@login_required
def report_found_dog(request):
    if request.method == 'POST':
        form = FoundDogForm(request.POST, request.FILES)
        if form.is_valid():
            found_dog = form.save(commit=False)
            found_dog.user = request.user

            # Get lat/lng from POST (from hidden fields in the template)
            lat = request.POST.get('found_latitude')
            lng = request.POST.get('found_longitude')

            if lat and lng:
                try:
                    found_dog.found_latitude = float(lat)
                    found_dog.found_longitude = float(lng)
                except ValueError:
                    messages.warning(request, "Invalid location data, saved without coordinates.")

            found_dog.save()
            messages.success(request, "Found dog reported.")
            return redirect('found_dogs_list')
        else:
            messages.error(request, "Please fix the form errors.")
    else:
        form = FoundDogForm()

    return render(request, 'lost/report_found_dog.html', {'form': form})

def found_dog_detail(request, pk):
    dog = get_object_or_404(FoundDog, pk=pk)
    return render(request, 'lost/found_dog_detail.html', {'dog': dog})

@login_required
def manage_found_dog(request, pk):
    dog = get_object_or_404(FoundDog, pk=pk)
    return render(request, 'lost/manage_found_dog.html', {'dog': dog})

@login_required
def edit_found_dog(request, pk):
    dog = get_object_or_404(FoundDog, pk=pk)
    if dog.matched:
        messages.warning(request, "Cannot edit. Dog already matched.")
        return redirect('manage_found_dog', pk=dog.pk)
    if request.method == 'POST':
        form = FoundDogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, "Report updated.")
            return redirect('manage_found_dog', pk=dog.pk)
        else:
            messages.error(request, "Update failed. Check for errors.")
    else:
        form = FoundDogForm(instance=dog)
    return render(request, 'lost/edit_found_dog.html', {'form': form, 'dog': dog})

@login_required
def delete_found_dog(request, pk):
    dog = get_object_or_404(FoundDog, pk=pk)
    if request.method == 'POST':
        dog.delete()
        messages.success(request, "Found dog entry deleted.")
        return redirect('found_dogs_list')
    return render(request, 'lost/delete_found_dog.html', {'dog': dog})

@login_required
def mark_found_dog_matched(request, pk):
    dog = get_object_or_404(FoundDog, pk=pk)
    if request.user != dog.user:
        messages.error(request, "Not authorized to mark this dog.")
        return redirect('found_dog_detail', pk=dog.pk)
    if dog.matched:
        messages.info(request, "Already marked as matched.")
        return redirect('manage_found_dog', pk=dog.pk)
    if request.method == 'POST':
        dog.matched = True
        dog.save()
        messages.success(request, f"{dog} marked as matched.")
        return redirect('manage_found_dog', pk=dog.pk)
    return render(request, 'lost/confirm_mark_matched.html', {'dog': dog})
