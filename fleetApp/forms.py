from django import forms
from .models import Vehicle, Driver, Requestor, Request, ServiceProvider, Service


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
        
class RequestorForm(forms.ModelForm):
    class Meta:
        model = Requestor
        fields = ['name', 'contact', 'email_address']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'current_location',
            'destination',
            'purpose',
        ]
        
class RequestApprovalForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['vehicle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only allocated vehicles with drivers
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status="Allocated", driver__isnull=False)

class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['service_provider_name', 'address', 'contact', 'email_address']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['particular', 'quantity', 'cost', 'service_provider', 'vehicle']


class VehicleReturnForm(forms.Form):
    mileage_at_return = forms.IntegerField(
        label="Mileage at Return",
        required=True,
        min_value=0,
    )
