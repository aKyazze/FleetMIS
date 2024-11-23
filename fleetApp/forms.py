from django import forms
from .models import Vehicle, Driver, ServiceProvider, Service


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_plate', 'vehicle_type', 'engine_type', 'mileage']
        


class VehicleAllocationForm(forms.Form):
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        empty_label="Select a Driver"
    )

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['driver_name', 'gender', 'contact', 'email_address']
        
class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['service_provider_name', 'address', 'contact', 'email_address']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['particular', 'quantity', 'cost', 'service_provider', 'vehicle']


