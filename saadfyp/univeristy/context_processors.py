# from .models import Notification

# def notification_count(request):
#     if request.user.is_authenticated:
#         return {'notification_count': Notification.objects.filter(user=request.user, is_read=False).count()}
#     return {'notification_count': 0}


from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        notification_count = unread_notifications.count()
        return {
            'notification_count': notification_count,
            'unread_notifications': unread_notifications,
        }
    return {
        'notification_count': 0,
        'unread_notifications': [],
    }
