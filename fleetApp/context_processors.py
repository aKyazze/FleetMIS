from fleetApp.models import Alert

def unread_alerts_count(request):
    if request.user.is_authenticated and request.user.groups.filter(name="FleetManagers").exists():
        count = Alert.objects.filter(priority_level="High").count()
        return {'unread_alerts_count': count}
    return {}
