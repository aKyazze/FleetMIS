# Standard library imports

# Django imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission, User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Local app imports
from .models import Alert, Driver, GSMsensorData, Request, Requestor, Service, ServiceProvider, UserProfile, Vehicle, Department


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_plate', 'vehicle_type', 'engine_type', 'mileage']

    def __init__(self, *args, **kwargs):
        # Get instance for comparison during update
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_vehicle_plate(self):
        plate = self.cleaned_data['vehicle_plate'].upper().strip()
        qs = Vehicle.objects.filter(vehicle_plate__iexact=plate)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise ValidationError("This vehicle plate number already exists.")
        return plate

class VehicleAllocationForm(forms.Form):
    driver = forms.ModelChoiceField(queryset=Driver.objects.filter(vehicle__isnull=True))

class VehicleReturnForm(forms.Form):
    mileage_at_return = forms.IntegerField(
        label="Mileage at Return",
        required=True,
        min_value=0,
    )


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user', 'driver_name', 'gender', 'contact', 'email_address']
        widgets = {
            'user': forms.Select(attrs={'id': 'id_user'}),
            'driver_name': forms.TextInput(attrs={'readonly': True, 'id': 'id_name'}),  
            'email_address': forms.EmailInput(attrs={'readonly': True, 'id': 'id_email_address'}),
            'contact': forms.TextInput(attrs={'readonly': True, 'id': 'id_contact'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assigned_users = Driver.objects.exclude(user__isnull=True).values_list('user_id', flat=True)

        if self.instance and self.instance.pk and self.instance.user:
            # Editing: allow the already assigned user
            assigned_users = assigned_users.exclude(pk=self.instance.user.pk)

        self.fields['user'].queryset = User.objects.exclude(id__in=assigned_users)

        # If form is bound (e.g. POST with errors), include the selected user temporarily
        if 'user' in self.data:
            try:
                selected_user_id = int(self.data.get('user'))
                # Re-add the selected user if filtered out
                if selected_user_id not in self.fields['user'].queryset.values_list('id', flat=True):
                    selected_user = User.objects.filter(pk=selected_user_id).first()
                    if selected_user:
                        self.fields['user'].queryset |= User.objects.filter(pk=selected_user.pk)
            except (ValueError, TypeError):
                pass


class RequestorForm(forms.ModelForm):
    class Meta:
        model = Requestor
        fields = ['user', 'name', 'contact', 'email_address']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'email_address': forms.EmailInput(attrs={'readonly': True}),
            'contact': forms.TextInput(attrs={'readonly': True}),
        }

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    user_id = self.initial.get('user') or self.data.get('user')

    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            self.fields['name'].initial = f"{user.first_name} {user.last_name}".strip()
            self.fields['email_address'].initial = user.email

            # Corrected: use user.userprofile
            if hasattr(user, 'userprofile'):
                self.fields['contact'].initial = user.userprofile.contact

        except User.DoesNotExist:
            pass


class RequestForm(forms.ModelForm):
    required_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select the date when the vehicle is needed."
    )

    class Meta:
        model = Request
        fields = ['current_location', 'destination', 'purpose', 'required_date']

    def clean_required_date(self):
        required_date = self.cleaned_data.get('required_date')
        today = timezone.localdate()

        if required_date < today:
            raise forms.ValidationError("Required date cannot be in the past.")
        
        return required_date
class RequestApprovalForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['vehicle', 'driver']  # Include driver in approval form

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


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    contact = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)
    passport_photo = forms.ImageField(required=False)
    department = forms.ChoiceField(choices=Department.DEPARTMENT_LIST)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
class StaffEditForm(forms.ModelForm):
    contact = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)
    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
class UserCredentialForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permissions"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']