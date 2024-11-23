from django import forms
from .models import Vehicle, Driver


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
        

        

