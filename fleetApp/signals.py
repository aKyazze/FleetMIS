# Django imports
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save, user_logged_in
from django.dispatch import receiver

# Local app imports
from .models import Alert, GSMsensorData, Request, Requestor, Staff
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
        print("== Sending Trip Request Notification ==")
        print("Requestor:", getattr(instance.requestor, 'name', 'Unknown'))
        print("Destination:", instance.destination)
        print("Request Date:", instance.request_date)
        print("Required Date:", instance.required_date)  # Diagnostic line

        send_notification(
            subject='New Trip Request Pending',
            template_name='emails/pending_request_manager.html',
            context={
                'requestor': getattr(instance.requestor, 'name', 'Unknown'),
                'requestor_name': getattr(instance.requestor, 'name', 'Unknown'),
                'destination': instance.destination,
                'purpose': instance.purpose,
                'request_date': instance.request_date,
                'required_date': instance.required_date,
                'manager_name': "Fleet Manager"
            },
            recipient_email='fleetmanager@utcl.com'
        )

@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Staff.objects.get_or_create(user=instance)
