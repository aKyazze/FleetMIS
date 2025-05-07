
# This is the old Version

from django import forms
from .models import Vehicle, Driver, Requestor, Request, ServiceProvider, Service


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_plate', 'vehicle_type', 'engine_type', 'mileage']
        

    
class VehicleAllocationForm(forms.Form):
    driver = forms.ModelChoiceField(queryset=Driver.objects.filter(vehicle__isnull=True))
   # request = forms.ModelChoiceField(queryset=Request.objects.filter(request_status="P"))  # Pending requests only

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['driver_name', 'gender', 'contact', 'email_address']
        
class RequestorForm(forms.ModelForm):
    class Meta:
        model = Requestor
        fields = ['user','name', 'contact', 'email_address']

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
'''

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'contact', 'email_address']

class StaffRequestForm(forms.Form):
    current_location = forms.CharField(max_length=100)
    destination = forms.CharField(max_length=100)
    purpose = forms.CharField(widget=forms.Textarea)

class FleetManagerForm(forms.ModelForm):
    class Meta:
        model = FleetManager
        fields = ['manager_name', 'contact', 'email_address']

class GSMsensorDataForm(forms.ModelForm):
    class Meta:
        model = GSMsensorData
        fields = ['vehicle', 'sensor_type', 'data_value', 'timestamp', 'transmission_mode']

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['vehicle', 'sensor', 'alert_type', 'alert_message', 'trigger_source', 'priority_level', 'recipient_role', 'timestamp']
'''