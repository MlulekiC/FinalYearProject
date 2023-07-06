from .models import Notification
from django.db.models import Q

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(Q(to_user=request.user) & Q(is_read=False))
        return {'notifications': notifications}
    else:
        return {'notifications': []}