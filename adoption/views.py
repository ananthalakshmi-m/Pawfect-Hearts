from django.shortcuts import render, redirect, get_object_or_404
from .models import Dog
from .forms import DogForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages  # ✅ added for user messages

def adoption_list(request):
    breed = request.GET.get('breed')
    location = request.GET.get('location')

    dogs = Dog.objects.filter(is_adopted=False)

    if breed:
        dogs = dogs.filter(breed=breed)
    if location:
        dogs = dogs.filter(location=location)

    breeds = Dog.objects.filter(is_adopted=False).order_by('breed').values_list('breed', flat=True).distinct()
    locations = Dog.objects.filter(is_adopted=False).order_by('location').values_list('location', flat=True).distinct()

    context = {
        'dogs': dogs,
        'selected_breed': breed or '',
        'selected_location': location or '',
        'breeds': breeds,
        'locations': locations,
    }

    return render(request, 'adoption/adoption_list.html', context)

def dog_detail(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    return render(request, 'adoption/dog_detail.html', {'dog': dog})

@login_required
def add_dog(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.added_by = request.user
            dog.save()
            messages.success(request, "Dog added for adoption successfully.")
            return redirect('adoption_list')
    else:
        form = DogForm()
    return render(request, 'adoption/add_dog.html', {'form': form})

@login_required
def toggle_favorite(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    if request.user in dog.favorited_by.all():
        dog.favorited_by.remove(request.user)
        favorited = False
    else:
        dog.favorited_by.add(request.user)
        favorited = True
    return JsonResponse({'favorited': favorited})

@login_required
def favorite_dogs(request):
    dogs = request.user.favorite_dogs.all()
    return render(request, 'adoption/favorites.html', {'dogs': dogs})

@login_required
def manage_dog(request, pk):
    dog = get_object_or_404(Dog, pk=pk, added_by=request.user)
    return render(request, 'adoption/manage_dog.html', {'dog': dog})

@login_required
def toggle_adopted(request, pk):
    dog = get_object_or_404(Dog, pk=pk, added_by=request.user)
    if request.method == 'POST':
        dog.is_adopted = not dog.is_adopted
        dog.save()
        if dog.is_adopted:
            messages.success(request, "Dog marked as adopted.")
        else:
            messages.info(request, "Dog marked as available for adoption.")
    return redirect('user_dashboard')

@login_required
def edit_dog(request, pk):
    dog = get_object_or_404(Dog, pk=pk, added_by=request.user)

    if dog.is_adopted:
        messages.warning(request, "Cannot edit. This dog has already been adopted.")
        return redirect('manage_dog', pk=dog.pk)

    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, "Dog details updated successfully.")
            return redirect('manage_dog', pk=dog.pk)
        else:
            messages.error(request, "Error updating dog details. Please check the form.")
    else:
        form = DogForm(instance=dog)

    return render(request, 'adoption/edit_dog.html', {'form': form, 'dog': dog})

@login_required
def confirm_mark_adopted(request, pk):
    dog = get_object_or_404(Dog, pk=pk)

    if request.user != dog.added_by:
        messages.error(request, "You are not authorized to mark this dog.")
        return redirect('dog_detail', pk=dog.pk)

    if dog.is_adopted:
        messages.info(request, f"{dog.name} is already marked as adopted.")
        return redirect('manage_dog', pk=dog.pk)

    if request.method == 'POST':
        dog.is_adopted = True
        dog.save()
        messages.success(request, f"{dog.name} has been marked as adopted.")
        return redirect('manage_dog', pk=dog.pk)

    return render(request, 'adoption/confirm_mark_adopted.html', {'dog': dog})

@login_required
def delete_dog(request, pk):
    dog = get_object_or_404(Dog, pk=pk, added_by=request.user)

    if request.method == 'POST':
        dog.delete()
        messages.success(request, "Dog removed from the adoption list.")
        return redirect('user_dashboard')

    return render(request, 'adoption/confirm_delete.html', {'dog': dog})
