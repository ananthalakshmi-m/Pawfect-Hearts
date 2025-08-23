from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib import messages

@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-timestamp')
    return render(request, 'notifications_pane/notification_list.html', {
        'notifications': notifications
    })

@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save()

    if notification.target:
        return redirect(notification.target.get_absolute_url())
    messages.info(request, "The content linked to this notification is no longer available.")
    return redirect('notification_list')

@login_required
def mark_all_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notification_list')
