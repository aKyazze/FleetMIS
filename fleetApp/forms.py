
# This is the old Version

from django import forms
from django.contrib.auth.models import User
from .models import Vehicle, Driver, Requestor, Request, ServiceProvider, Service, GSMsensorData, Alert


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
        fields = ['user','driver_name', 'gender', 'contact', 'email_address']
        widgets = {
            'driver_name': forms.TextInput(attrs={'id': 'id_driver_name'}),
            'email_address': forms.EmailInput(attrs={'id': 'id_email_address'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assigned_users = Driver.objects.exclude(user__isnull=True).values_list('user_id', flat=True)

        if self.instance and self.instance.pk and self.instance.user:
            # Allow the current user to stay in the dropdown
            assigned_users = assigned_users.exclude(pk=self.instance.user.pk)

        self.fields['user'].queryset = User.objects.exclude(id__in=assigned_users)
        
        
class RequestorForm(forms.ModelForm):
    class Meta:
        model = Requestor
        fields = ['user','name', 'contact', 'email_address']
        
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'email_address': forms.EmailInput(attrs={'readonly': True}),
            'contact': forms.TextInput(attrs={'readonly': False}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Auto-fill if 'user' is in initial data
        user = self.initial.get('user') or self.data.get('user')
        if user:
            try:
                from django.contrib.auth.models import User
                user_obj = User.objects.get(pk=user)
                self.fields['name'].initial = f"{user_obj.first_name} {user_obj.last_name}".strip()
                self.fields['email_address'].initial = user_obj.email
                # contact isn't in User model — set manually later if needed
            except User.DoesNotExist:
                pass

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

class GSMsensorDataForm(forms.ModelForm):
    class Meta:
        model = GSMsensorData
        fields = ['vehicle', 'sensor_type', 'data_value', 'transmission_mode']

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['vehicle', 'sensor_data', 'alert_type', 'alert_message', 'trigger_source', 'priority_level', 'recipient_role']
