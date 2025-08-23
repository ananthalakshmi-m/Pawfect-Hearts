from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import DonorForm, BloodRequestForm
from .models import Donor, BloodRequest
from django.contrib import messages
from notifications_pane.models import Notification
from django.contrib.contenttypes.models import ContentType
from .utils import send_blood_request_email

def donor_list(request):
    donors = Donor.objects.filter(available = True)

    breed = request.GET.get('breed')
    blood_type = request.GET.get('blood_type')
    location = request.GET.get('location')

    if breed:
        donors = donors.filter(breed=breed)
    if blood_type:
        donors = donors.filter(blood_type=blood_type)
    if location:
        donors = donors.filter(location=location)

    context = {
        'donors': donors,
        'breeds': Donor.objects.values_list('breed', flat=True).distinct(),
        'blood_types': Donor.objects.values_list('blood_type', flat=True).distinct(),
        'locations': Donor.objects.values_list('location', flat=True).distinct(),
    }
    return render(request, 'blood/donor_list.html', context)


@login_required
def register_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, "Donor profile created successfully.")
            return redirect('donor_list')
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        form = DonorForm()
    return render(request, 'blood/register_donor.html', {'form': form})


@login_required
def request_blood(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.user = request.user
            blood_request.save()
            notify_donors(blood_request)
            messages.success(request, "Blood request submitted successfully.")
            return redirect('blood_requests')
        else:
            messages.error(request, "There was an error submitting your request.")
    else:
        form = BloodRequestForm()
    return render(request, 'blood/request_blood.html', {'form': form})


def blood_requests(request):
    requests = BloodRequest.objects.filter(is_fulfilled = False).order_by('-date_requested')
    return render(request, 'blood/blood_requests.html', {'requests': requests})


def notify_donors(blood_request):
    matching_donors = Donor.objects.filter(
        blood_type=blood_request.blood_type_needed,
        available=True
    )

    blood_request_ct = ContentType.objects.get_for_model(blood_request)

    for donor in matching_donors:
        if not donor.email:
            continue

        try:
            send_blood_request_email(donor.email, blood_request.blood_type_needed, donor.dog_name)
        except Exception:
            pass

        exists = Notification.objects.filter(
            user=donor.user,
            content_type=blood_request_ct,
            object_id=blood_request.id,
            message__icontains=f"{donor.dog_name}"
        ).exists()

        if not exists:
            notification_message = (
                f"A new blood request needs a donor with blood type {blood_request.blood_type_needed} "
                f"for your dog {donor.dog_name}."
            )

            Notification.objects.create(
                user=donor.user,
                message=notification_message,
                content_type=blood_request_ct,
                object_id=blood_request.id
            )


def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    return render(request, 'blood/donor_detail.html', {'donor': donor})


@login_required
def manage_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk, user=request.user)
    return render(request, 'blood/manage_donor.html', {'donor': donor})

@require_POST
@login_required
def toggle_donor_availability(request, pk):
    donor = get_object_or_404(Donor, pk=pk, user=request.user)
    donor.available = not donor.available
    donor.save()
    return redirect('manage_donor', pk=donor.pk)

@login_required
def edit_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk, user=request.user)
    
    if request.method == 'POST':
        original_available = donor.available
        form = DonorForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            updated_donor = form.save(commit=False)
            updated_donor.available = original_available
            updated_donor.save()
            messages.success(request, "Donor info updated successfully.")
            return redirect('manage_donor', pk=pk)
        else:
            messages.error(request, "Error updating donor info. Please check the form.")
    else:
        form = DonorForm(instance=donor)

    return render(request, 'blood/edit_donor.html', {'form': form, 'donor': donor})

@login_required
def delete_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk, user=request.user)
    if request.method == 'POST':
        donor.delete()
        messages.success(request, "Donor deleted successfully.")
        return redirect('user_dashboard')
    return render(request, 'blood/delete_donor.html', {'donor': donor})


def request_detail(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    return render(request, 'blood/request_detail.html', {'blood_request': blood_request})


@login_required
def manage_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)

    if blood_request.user != request.user:
        messages.error(request, "You do not have permission to manage this request.")
        return redirect('blood_requests')

    if request.method == 'POST' and 'mark_as_resolved' in request.POST:
        blood_request.status = 'fulfilled'
        blood_request.save()
        messages.success(request, "Blood request marked as fulfilled.")
        return redirect('blood_requests')

    return render(request, 'blood/manage_request.html', {'blood_request': blood_request})


@login_required
def delete_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)

    if blood_request.user != request.user:
        messages.error(request, "You do not have permission to delete this request.")
        return redirect('blood_requests')

    if request.method == 'POST':
        blood_request.delete()
        messages.success(request, "Blood request deleted successfully.")
        return redirect('user_dashboard')

    return render(request, 'blood/delete_request.html', {'blood_request': blood_request})


@login_required
def confirm_fulfill_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk, user=request.user)
    return render(request, 'blood/confirm_fulfill.html', {'blood_request': blood_request})


@login_required
def fulfill_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk, user=request.user)

    if request.method == 'POST':
        blood_request.is_fulfilled = True
        blood_request.save()
        messages.success(request, "Request marked as fulfilled.")
        return redirect('manage_request', pk=pk)

    return redirect('confirm_fulfill_request', pk=pk)
