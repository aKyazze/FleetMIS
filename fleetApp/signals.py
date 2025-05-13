# Django imports
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, user_logged_in
from django.dispatch import receiver

# Local app imports
from .models import Alert, GSMsensorData, Request, Requestor
from fleetApp.utils.email_utils import send_notification


@receiver(user_logged_in)
def create_requestor_profile(sender, request, user, **kwargs):
    if user.groups.filter(name='FleetUsers').exists():
        Requestor.objects.get_or_create(user=user)

#logic to check thresholds when saving sensor data:

@receiver(post_save, sender=GSMsensorData)
def generate_alert(sender, instance, created, **kwargs):
    if not created:
        return  # only create alert for new records

    # Threshold logic for different sensor types
    if instance.sensor_type == "Fuel" and instance.data_value < 10:
        Alert.objects.create(
            vehicle=instance.vehicle,
            sensor_data=instance,
            alert_type="Low Fuel",
            alert_message=f"Fuel level is critically low ({instance.data_value}L)",
            trigger_source="Sensor Data",
            priority_level="High",
            recipient_role="Fleet Manager"
        )
    elif instance.sensor_type == "Speed" and instance.data_value > 120:
        Alert.objects.create(
            vehicle=instance.vehicle,
            sensor_data=instance,
            alert_type="Overspeed",
            alert_message=f"Overspeeding detected ({instance.data_value} km/h)",
            trigger_source="Sensor Data",
            priority_level="High",
            recipient_role="Fleet Manager"
        )
    elif instance.sensor_type == "Engine" and instance.data_value > 100:
        Alert.objects.create(
            vehicle=instance.vehicle,
            sensor_data=instance,
            alert_type="High Temp",
            alert_message=f"Engine temperature too high ({instance.data_value} °C)",
            trigger_source="Sensor Data",
            priority_level="Medium",
            recipient_role="Fleet Manager"
        )
        
#logic for Email Notifications:
@receiver(post_save, sender=Request)
def notify_pending_request(sender, instance, created, **kwargs):
    if created and instance.request_status == "P":
        send_notification(
            subject='New Trip Request Pending',
            template_name='emails/pending_request_manager.html',
            context={
                'requestor': instance.requestor.name,
                'destination': instance.destination,
                'request_date': instance.request_date
            },
            recipient_email='fleetmanager@utcl.com'
        )
