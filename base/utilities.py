from .models import Notification

def create_notification(request, to_user, notification_type, extra_id=0):
    if to_user:
        for user in to_user:
            notification = Notification.objects.create(to_user=user, notification_type=notification_type, from_user=request.user, extra_id=extra_id)