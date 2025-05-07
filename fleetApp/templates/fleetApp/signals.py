# fleetApp/signals.py
from django.contrib.auth.models import Group
from django.db.models.signals import user_logged_in
from django.dispatch import receiver
from .models import Requestor

@receiver(user_logged_in)
def create_requestor_profile(sender, request, user, **kwargs):
    if user.groups.filter(name='FleetUsers').exists():
        Requestor.objects.get_or_create(user=user)
