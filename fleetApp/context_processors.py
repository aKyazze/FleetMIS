from fleetApp.models import Alert, Request

def unread_alerts_count(request):
    if request.user.is_authenticated and request.user.groups.filter(name="FleetManagers").exists():
        count = Alert.objects.filter(priority_level="High").count()
        return {'unread_alerts_count': count}
    return {}

def requisition_notifications(request):
    if request.user.is_authenticated and request.user.groups.filter(name='FleetManagers').exists():
        pending_reqs_count = Request.objects.filter(request_status='P').count()
        return {'pending_reqs_count': pending_reqs_count}
    return {}