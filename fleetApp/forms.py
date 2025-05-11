from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Vehicle, Driver, Requestor, Request, ServiceProvider, Service, GSMsensorData, Alert


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_plate', 'vehicle_type', 'engine_type', 'mileage']
        
    def clean_vehicle_plate(self):
        plate = self.cleaned_data['vehicle_plate'].upper().strip()
        if Vehicle.objects.filter(vehicle_plate__iexact=plate).exists():
            raise ValidationError("This vehicle plate number already exists.")
        return plate


class VehicleAllocationForm(forms.Form):
    driver = forms.ModelChoiceField(queryset=Driver.objects.filter(vehicle__isnull=True))
    # You can add more fields here like request, vehicle, etc., if needed.


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user', 'driver_name', 'gender', 'contact', 'email_address']
        widgets = {
            'driver_name': forms.TextInput(attrs={'id': 'id_driver_name'}),
            'email_address': forms.EmailInput(attrs={'id': 'id_email_address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assigned_users = Driver.objects.exclude(user__isnull=True).values_list('user_id', flat=True)

        if self.instance and self.instance.pk and self.instance.user:
            assigned_users = assigned_users.exclude(pk=self.instance.user.pk)

        self.fields['user'].queryset = User.objects.exclude(id__in=assigned_users)


class RequestorForm(forms.ModelForm):
    class Meta:
        model = Requestor
        fields = ['user', 'name', 'contact', 'email_address']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'email_address': forms.EmailInput(attrs={'readonly': True}),
            'contact': forms.TextInput(attrs={'readonly': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.initial.get('user') or self.data.get('user')
        if user:
            try:
                user_obj = User.objects.get(pk=user)
                self.fields['name'].initial = f"{user_obj.first_name} {user_obj.last_name}".strip()
                self.fields['email_address'].initial = user_obj.email
            except User.DoesNotExist:
                pass


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['current_location', 'destination', 'purpose']


class RequestApprovalForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['vehicle', 'driver']  # ✅ Include driver in approval form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status="Allocated")
        self.fields['driver'].queryset = Driver.objects.all()  # You can filter based on custom logic


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
        fields = [
            'vehicle', 'sensor_data', 'alert_type', 'alert_message',
            'trigger_source', 'priority_level', 'recipient_role'
        ]
