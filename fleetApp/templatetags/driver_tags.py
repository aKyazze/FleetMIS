# fleetApp/templatetags/driver_tags.py
from django import template
from fleetApp.models import Driver

register = template.Library()

@register.filter
def get_driver_for_vehicle(drivers, vehicle):
    return drivers.filter(vehicle=vehicle).first()
