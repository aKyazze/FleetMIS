# Standard library imports
import base64
import csv

# Third-party imports
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import RequestCreateSerializer, RequestReadSerializer
from xhtml2pdf import pisa
from io import BytesIO

# Django imports
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required, 
    permission_required, 
    user_passes_test
)
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import Group, Permission, User
from django.core.files.base import ContentFile
from django.db.models import ExpressionWrapper, F, IntegerField, Q
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.views.decorators.http import require_GET


# Local application imports
from fleetApp.utils.email_utils import send_notification
from .forms import (
    AlertForm, DriverForm, GroupForm, GSMsensorDataForm,
    RequestApprovalForm, RequestForm, RequestorForm,
    ServiceForm, ServiceProviderForm, StaffEditForm,
    UserCredentialForm, UserProfileForm, 
    VehicleAllocationForm, VehicleForm, VehicleReturnForm
)
from .models import (
    Alert, Driver, GSMsensorData, Request, Requestor,
    Service, ServiceProvider, UserProfile, Vehicle
)


# Create your views here.
############################################################################################
######################### LOGIN VIEWS #####################################################
@login_required
def login_redirect_view(request):
    user = request.user
    if user.groups.filter(name='Admins').exists():
        return redirect('admin_dashboard')
    elif user.groups.filter(name='FleetManagers').exists():
        return redirect('fleet_manager_dashboard')
    elif user.groups.filter(name='FleetUsers').exists():
        return redirect('fleet_user_dashboard')
    else:
        return redirect('default_dashboard')  # Optional fallback
    

def is_admin(user):
    return user.groups.filter(name='Admins').exists()

@user_passes_test(is_admin)
def admin_dashboard(request):
    ...

def is_fleet_manager(user):
    return user.groups.filter(name='FleetManagers').exists()

@user_passes_test(is_fleet_manager)
def fleet_dashboard(request):
    ...

@login_required
def user_requests(request):
    # Get filter from query string (?status=pending or ?status=closed)
    status_filter = request.GET.get('status')

    # Apply filter logic
    if status_filter == 'pending':
        requests = Request.objects.filter(requestor=request.user, request_status='P')
    elif status_filter == 'closed':
        requests = Request.objects.filter(requestor=request.user, request_status='C')
    else:
        requests = Request.objects.filter(requestor=request.user)

    # Pass selected status for template use (e.g., UI highlighting)
    context = {
        'requests': requests,
        'selected_status': status_filter
    }

    return render(request, 'fleetApp/requisition/user_requests.html', context)

################################################################################################################
######################################## SECTION FOR Registration Views ########################################

def sign_up_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User signed up successfully!")
            return redirect('login')
        else:
            messages.error(request, "Sign up failed. Please check the form.")
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up.html', context)

@login_required
def custom_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})
# views.py

@login_required
def register_step1(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Store form data in session (only serializable data)
            request.session['registration_data'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'contact': form.cleaned_data['contact'],
                'gender': form.cleaned_data['gender'],
                'department_id': form.cleaned_data['department'],
            }

            # Handle passport photo
            photo_file = request.FILES.get('passport_photo')
            if photo_file:
                photo_data = base64.b64encode(photo_file.read()).decode('utf-8')
                request.session['has_photo'] = True
                request.session['photo_name'] = photo_file.name
                request.session['photo_data'] = photo_data
            else:
                request.session['has_photo'] = False
                request.session['photo_name'] = None
                request.session['photo_data'] = None

            request.session.modified = True  # Mark session as changed
            return redirect('register_step2')
    else:
        form = UserProfileForm()

    return render(request, 'fleetApp/base/register_step1.html', {'form': form})


@login_required
def register_step2(request):
    data = request.session.get('registration_data')
    if not data:
        return redirect('register_step1')

    if request.method == 'POST':
        form = UserCredentialForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            department_code = data['department_id']
            user.save()

            # Create UserProfile
            profile = UserProfile.objects.create(
                user=user,
                contact=data['contact'],
                gender=data['gender'],
                department=department_code,
            )

            # Save passport photo if available

            if request.session.get('has_photo') and request.session.get('photo_data'):
                photo_data = base64.b64decode(request.session['photo_data'])
                photo_name = request.session.get('photo_name', 'photo.jpg')
                profile.passport_photo.save(photo_name, ContentFile(photo_data))

            # Create or update Staff record
            from fleetApp.models import Staff  # Ensure correct import

            staff, created = Staff.objects.get_or_create(user=user)
            staff.first_name = user.first_name
            staff.last_name = user.last_name
            staff.email = user.email
            staff.contact = data['contact']
            staff.gender = data['gender']
            staff.department = department_code
            if profile.passport_photo:
                staff._photo = profile.passport_photo
            staff.save()

            # Assign group
            selected_group = form.cleaned_data.get('group')
            if selected_group:
                user.groups.add(selected_group)

            # Clean up session
            for key in ['registration_data', 'has_photo', 'photo_name', 'photo_data']:
                request.session.pop(key, None)

            messages.success(request, f"User {user.username} created successfully.")
            return redirect('staff_dashboard')
    else:
        initial_username = data['first_name'].lower()
        form = UserCredentialForm(initial={'username': initial_username})

    return render(request, 'fleetApp/base/register_step2.html', {'form': form})


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'fleetApp/base/user_list.html', {'users': users})

@login_required
def staff_dashboard(request):
    users = User.objects.select_related('userprofile').all()
    return render(request, 'fleetApp/base/staff_dashboard.html', {'users': users})


@login_required
def edit_staff(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # Update user basic info
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.save()

            # Update profile info
            profile.contact = data['contact']
            profile.gender = data['gender']
            profile.department = data['department']
            if request.FILES.get('passport_photo'):
                profile.passport_photo = request.FILES['passport_photo']
            profile.save()

            # Update user groups
            selected_groups = set(data['groups'])
            current_groups = set(user.groups.all())

            to_add = selected_groups - current_groups
            to_remove = current_groups - selected_groups

            for group in to_add:
                user.groups.add(group)

            for group in to_remove:
                user.groups.remove(group)

            messages.success(request, "Staff updated successfully with group assignments.")
            return redirect('staff_dashboard')
    else:
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'contact': profile.contact,
            'gender': profile.gender,
            'groups': user.groups.all(),
        }
        form = UserProfileForm(initial=initial)

    return render(request, 'fleetApp/base/edit_staff.html', {
        'form': form,
        'user_obj': user,
        'photo': profile.passport_photo.url if profile.passport_photo else None,
    })


@login_required
def delete_staff(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    if user_to_delete == request.user:
        # User trying to delete themselves
        return render(request, 'fleetApp/base/delete_staff.html', {
            'user_obj': user_to_delete,
            'error_message': "⚠️ You cannot delete an Admin account."
        })

    if request.method == "POST":
        user_to_delete.delete()
        messages.success(request, "Staff deleted successfully.")
        return redirect('staff_dashboard')

    return render(request, 'fleetApp/base/delete_staff.html', {'user_obj': user_to_delete})

@login_required
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            fleet_users_group = Group.objects.get(name="FleetUsers")
            user.groups.add(fleet_users_group)

            # Create a corresponding Requestor profile
            Requestor.objects.get_or_create(user=user)
            
            messages.success(request, "User registered and added to staff list.")
            return redirect("requestor_list")
        
@login_required
@permission_required('auth.add_group', raise_exception=True)
def add_group_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created successfully with permissions.")
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'fleetApp/base/add_group.html', {'form': form})

@login_required
@permission_required('auth.view_group', raise_exception=True)
def group_list_view(request):
    groups = Group.objects.all().prefetch_related('permissions')
    return render(request, 'fleetApp/base/group_list.html', {'groups': groups})

@login_required
def edit_group_permissions(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    all_permissions = Permission.objects.all()
    assigned_permissions = group.permissions.all()
    available_permissions = all_permissions.exclude(id__in=assigned_permissions)

    if request.method == 'POST':
        selected_ids = request.POST.get('selected_permissions', '')
        selected_ids = [int(i) for i in selected_ids.split(',') if i]

        group.permissions.set(Permission.objects.filter(id__in=selected_ids))
        messages.success(request, f"Permissions updated for group '{group.name}'.")
        return redirect('group_list')

    context = {
        'group': group,
        'assigned_permissions': assigned_permissions,
        'available_permissions': available_permissions,
    }
    return render(request, 'fleetApp/base/edit_group_permissions.html', context)

@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    all_perms = Permission.objects.all()

    if request.method == 'POST':
        group.name = request.POST.get('name')
        group.save()
        group.permissions.set(request.POST.getlist('permissions'))
        messages.success(request, "Group updated successfully.")
        return redirect('group_list')

    return render(request, 'fleetApp/base/edit_group.html', {
        'group': group,
        'permissions': all_perms,
    })

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, "Group deleted successfully.")
        return redirect('group_list')
    return render(request, 'fleetApp/base/delete_group.html', {'group': group})


#This is Backend API Endpoints SECTION 
# 
# endpoint view to return user Details by ID
@require_GET
@login_required
def get_user_info(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'name': f"{user.first_name} {user.last_name}".strip(),
            'email': user.email,
            'contact': user.userprofile.contact if hasattr(user, 'userprofile') else '',
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user

        if user.groups.filter(name="FleetDriver").exists():
            role = "FleetDriver"
        elif user.groups.filter(name="FleetUsers").exists():
            role = "FleetUser"
        else:
            role = "Unknown"

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'role': role
        }
    )
        
 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fleet_dashboard_api(request):
    user = request.user
    name = user.get_full_name() or user.username

    response_data = {
        "name": name,
        "role": None,
    }

    if user.groups.filter(name="FleetUsers").exists() or user.groups.filter(name="FleetDrivers").exists():
        # Basic user / driver view
        pending = Request.objects.filter(requestor=user, request_status="P").count()
        approved = Request.objects.filter(requestor=user, request_status="O").count()
        completed = Request.objects.filter(requestor=user, request_status="C").count()

        response_data.update({
            "role": "FleetUser",
            "pendingRequests": pending,
            "approvedRequests": approved,
            "completedRequests": completed,
        })

    elif user.groups.filter(name="FleetManagers").exists() or user.is_superuser:
        # Manager or admin view
        totalVehicles = Vehicle.objects.count()
        totalDrivers = Driver.objects.count()
        totalRequestors = Requestor.objects.count()
        totalServices = Service.objects.count()
        totalServiceProviders = ServiceProvider.objects.count()
        totalPendingRequests = Request.objects.filter(request_status="P").count()
        totalCompletedRequests = Request.objects.filter(request_status="C").count()
        unreadAlerts = Alert.objects.filter(read=False).count()

        response_data.update({
            "role": "FleetManager",
            "totalVehicles": totalVehicles,
            "totalDrivers": totalDrivers,
            "totalRequestors": totalRequestors,
            "totalServices": totalServices,
            "totalServiceProviders": totalServiceProviders,
            "totalPendingRequests": totalPendingRequests,
            "totalCompletedRequests": totalCompletedRequests,
            "unreadAlertsCount": unreadAlerts,
        })

    else:
        response_data["role"] = "None"
        response_data["message"] = "You do not have dashboard access"

    return JsonResponse(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vehicle_request(request):
    """
    Create a new trip request. Converts camelCase input from frontend to snake_case.
    """
    user = request.user
    data = request.data

    # Normalize camelCase → snake_case
    payload = {
        "requestor": user.id,
        "current_location": data.get("currentLocation"),
        "destination": data.get("destination"),
        "purpose": data.get("purpose"),
        "required_date": data.get("requiredDate"),
        "request_status": "P",
    }

    print("Normalized Payload Received:", payload)

    serializer = RequestCreateSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Request submitted successfully"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_requests(request):
    """
    Returns all requests made by the currently authenticated user.
    """
    requests = Request.objects.filter(requestor=request.user).order_by('-request_date')
    serializer = RequestReadSerializer(requests, many=True)
    return Response(serializer.data)

####################################################################################################
##################################### MAIN & HOME SECTION ##########################################

#This is the Main view
@login_required
def main_view(request):
    return render(request, 'main.html')

#This is Home View
@login_required
def home_view(request):
    user = request.user
    context = {}

    # FleetUsers - Requestors
    if user.groups.filter(name="FleetUsers").exists():
        pending_requests = Request.objects.filter(requestor=user, request_status="P")
        approved_requests = Request.objects.filter(requestor=user, request_status="O") 
        completed_requests = Request.objects.filter(requestor=user, request_status="C").select_related('vehicle')

        for req in completed_requests:
            req.assigned_driver = Driver.objects.filter(vehicle=req.vehicle).first() if req.vehicle else None

        context.update({
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'completed_requests': completed_requests,
        })

    # FleetDrivers - Assigned Trips
    elif user.groups.filter(name="FleetDrivers").exists():
        driver = Driver.objects.filter(email_address=user.email).first()
        assigned_vehicle = Vehicle.objects.filter(driver=driver).first() if driver else None

        open_trips = Request.objects.filter(driver=driver, request_status="O")
        past_trips = Request.objects.filter(driver=driver, request_status="C")

        context.update({
            'driver': driver,
            'assigned_vehicle': assigned_vehicle,
            'open_trips': open_trips,
            'past_trips': past_trips,
        })

    # Admins / FleetManagers - General dashboard
    else:
        context.update({
            'total_vehicles': Vehicle.objects.count(),
            'total_drivers': Driver.objects.count(),
            'total_pending_requests': Request.objects.filter(request_status="P").count(),
            'total_completed_requests': Request.objects.filter(request_status="C").count(),
            'total_services': Service.objects.count(),
            'total_requestors': Requestor.objects.count(),
            'total_service_providers': ServiceProvider.objects.count(),
        })

    return render(request, 'fleetApp/base/home.html', context)

############################################################################################
################################### This Section for Vehicle Views #########################
# Create or Add a New Vehicle View
@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle added successfully!")
            return redirect('vehicle')
        else:
            messages.error(request, "This vehicle plate number already exists.")
            return redirect('vehicle')
    else:
        form = VehicleForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/vehicle/add_vehicle.html', context)

#Vehicle List
@login_required
def vehicle_view(request):
    # Get all vehicles
    vehicles = Vehicle.objects.all()
    drivers = Driver.objects.all()
    # Get all closed requests and annotate usage
    requests = Request.objects.filter(request_status="C").annotate(
        usage_summary=ExpressionWrapper(
            F('mileage_at_return') - F('mileage_at_assignment'), 
            output_field=IntegerField()
        )
    )
    context = {
        'vehicles': vehicles,
        'requests': requests,
        'drivers': drivers,
    }
    return render(request, 'fleetApp/vehicle/vehicles.html', context)

# Update or Edit Vehicle View
@login_required
def vehicle_update(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle Updated successfully!")
            return redirect('vehicle')
        else:
            messages.error(request, "Failed to Update vehicle. Please check the form.")
            return redirect('vehicle')
    else:
        form = VehicleForm(instance=vehicle)
    context = {
        'form': form, 
        'vehicle': vehicle
    }
    return render(request, 'fleetApp/vehicle/edit_vehicle.html', context)

# Delete Vehicle View 
@login_required
def vehicle_delete(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfully!")
        return redirect('vehicle')
    else:
        context = {'vehicle': vehicle}
        return render(request, 'fleetApp/vehicle/vehicle_confirm_delete.html', context)

# Assign or Allocate a Vehicle View 
@login_required
def allocate_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        form = VehicleAllocationForm(request.POST)
        if form.is_valid():
            driver = form.cleaned_data['driver']

            # Allocate the vehicle to the selected driver
            driver.vehicle = vehicle
            driver.save()

            # Update vehicle status
            vehicle.status = "Allocated"
            vehicle.save()

            messages.success(request, "Vehicle allocated successfully!")
            return redirect('vehicle')
        else:
            messages.error(request, "Failed to allocate vehicle. Please check the form.")
    else:
        form = VehicleAllocationForm()

    context = {
        'form': form,
        'vehicle': vehicle
    }
    return render(request, 'fleetApp/vehicle/allocate_vehicle.html', context)


# Return Vehicle View 
@login_required
def return_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == "POST":
        form = VehicleReturnForm(request.POST)
        if form.is_valid():
            mileage_at_return = form.cleaned_data['mileage_at_return']
            
            # Update vehicle and related data
            vehicle.status = 'Available'
            vehicle.mileage = mileage_at_return
            vehicle.save()

            driver = Driver.objects.filter(vehicle=vehicle).first()
            if driver:
                driver.vehicle = None
                driver.save()

            request_obj = Request.objects.filter(vehicle=vehicle, request_status="O").first()
            if request_obj:
                request_obj.mileage_at_return = mileage_at_return
                request_obj.request_status = "C"
                request_obj.save()

            # Send notification to all Fleet Managers
            try:
                fleet_manager_group = Group.objects.get(name="FleetManagers")
                managers = fleet_manager_group.user_set.all()

                for manager in managers:
                    if manager.email:
                        send_notification(
                            subject='Vehicle Returned',
                            template_name='emails/trip_returned_manager.html',
                            context={
                                'manager_name': manager.get_full_name() or manager.username,
                                'vehicle': vehicle.vehicle_plate,
                                'driver': driver.driver_name if driver else "Unknown",
                                'mileage': mileage_at_return,
                                'time': timezone.now().strftime("%H:%M %p"),
                            },
                            recipient_email=manager.email
                        )
            except Group.DoesNotExist:
                pass  # Fail silently if group doesn't exist

            messages.success(request, "Vehicle returned successfully!")
            return redirect('trip_history')
        else:
            messages.error(request, "Failed to return vehicle. Please check the form.")
    else:
        form = VehicleReturnForm()

    return render(request, 'fleetApp/vehicle/return_vehicle.html', {'vehicle': vehicle, 'form': form})

#############################################################################################################
######################################## SECTION FOR Driver Views ###########################################

# New Driver View 
@login_required
def driver_profile_view(request):
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        messages.error(request, "Driver profile not found.")
        return redirect('home')  # or any fallback page

    return render(request, 'fleetApp/driver/driver_profile.html', {'driver': driver})


@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver added successfully!")
            return redirect('drivers')
        else:
            messages.error(request, "Failed to add driver. Please check the form.")
    else:
        form = DriverForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/driver/add_driver.html', context)

# Driver List View 
@login_required
def drivers_list(request):
    #drivers = Driver.objects.select_related('vehicle').all()  
    drivers = Driver.objects.select_related('user').all()
    
    for driver in drivers:
        if not driver.vehicle:
            driver.vehicle_plate = "Unassigned"  
        else:
            driver.vehicle_plate = driver.vehicle.vehicle_plate  
    form = DriverForm()  
    context = {
        'drivers': drivers,
        'form': form
    }
    return render(request, 'fleetApp/driver/drivers.html', context)

# Driver Update View 
@login_required
def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver updated successfully!")
            return redirect('drivers')
        else:
            messages.error(request, "Failed to update driver. Please check the form.")
    else:
        form = DriverForm(instance=driver)
    context = {
        'form': form, 
        'driver': driver,
    }
    return render(request, 'fleetApp/driver/edit_driver.html', context)

# Driver Removing View 
@login_required
def delete_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        driver.delete()
        messages.success(request, "Driver deleted successfully!")
        return redirect('drivers')
    else:
        messages.error(request, "Failed to delete driver. Please try again.")
    context = {
        'driver': driver
    }
    return render(request, 'fleetApp/driver/driver_delete.html', context)

###############################################################################################################
######################################## SECTION FOR Requestor Views ########################################

# Add a requestor
@login_required
def add_requestor(request):
    if request.method == 'POST':
        form = RequestorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Requestor added successfully!")
            return redirect('requestor_list')
        else:
            messages.error(request, "Failed to add requestor. Please check the form.")
    else:
        form = RequestorForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/requisition/add_requestor.html', context)

@login_required
def get_user_info(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
        profile = getattr(user, 'userprofile', None)
        return JsonResponse({
            'name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'contact': profile.contact if profile else ''
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
# List all requestors
@login_required
def requestor_list(request):
    requestors = Requestor.objects.all()
    context = {
        'requestors': requestors
    }
    return render(request, 'fleetApp/requisition/requestor_list.html', context)

# Update Requestor
@login_required
def edit_requestor(request, requestor_id):
    requestor = get_object_or_404(Requestor, id=requestor_id)
    if request.method == 'POST':
        form = RequestorForm(request.POST, instance=requestor)
        if form.is_valid():
            form.save()
            messages.success(request, "Requestor updated successfully!")
            return redirect('requestor_list')
        else:
            messages.error(request, "Failed to update requestor. Please check the form.")
    else:
        form = RequestorForm(instance=requestor)
    context = {
        'form': form, 
        'requestor': requestor
    }
    return render(request, 'fleetApp/requisition/edit_requestor.html', context)

@login_required
def delete_requestor(request, requestor_id):
    requestor = get_object_or_404(Requestor, id=requestor_id)
    if request.method == 'POST':
        requestor.delete()
        messages.success(request, "Requestor deleted successfully!")
        return redirect('requestor_list')
    context = {
        'requestor': requestor
    }
    return render(request, 'fleetApp/requisition/delete_requestor.html', context)

##################################################################################################################
################################################## SECTION FOR Requests VIEWS ##########################################
@login_required
def requisitions_view(request):
    requestors = Requestor.objects.all()
    requests = Request.objects.select_related('requestor', 'vehicle').all()
    vehicles = Vehicle.objects.filter(status="Allocated")  
    approved_requests = Request.objects.filter(request_status="O")
    pending_requests = Request.objects.filter(request_status="P")

    requestor_form = RequestorForm()
    context = {
        'requestors': requestors,
        'requests': requests,
        'vehicles': vehicles,
        'approved_requests': approved_requests,
        "pending_requests": pending_requests,
        'requestor_form': requestor_form,
    }
    return render(request, 'fleetApp/requisition/requisitions.html', context)


@login_required
def add_request(request):
    try:
        requestor = request.user.requestor  
    except Requestor.DoesNotExist:
        messages.error(request, "No requestor profile found for this user.")
        return redirect('home')

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.requestor = request.user
            new_request.request_status = 'P'  
            new_request.save()

            #Notify Fleet Managers about new request
            try:
                fleet_manager_group = Group.objects.get(name='FleetManagers')
                fleet_managers = fleet_manager_group.user_set.all()

                for manager in fleet_managers:
                    if manager.email:
                        send_notification(
                            subject='New Trip Request Submitted',
                            template_name='emails/new_request_manager.html',
                            context={
                                'manager_name': manager.get_full_name() or manager.username,
                                'requestor_name': request.user.get_full_name() or request.user.username,
                                'destination': new_request.destination,
                                'purpose': new_request.purpose,
                                'request_date': new_request.request_date,
                            },
                            recipient_email=manager.email
                        )
            except Group.DoesNotExist:
                # Skip if group is not found, avoid breaking the request flow
                pass

            messages.success(request, "Request added successfully!")
            return redirect('user_requests')
    else:
        form = RequestForm()

    context = {
        'form': form,
        'requestor': requestor
    }
    return render(request, 'fleetApp/requisition/add_request.html', context)


@login_required
def edit_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            messages.success(request, "Request updated successfully!")
            return redirect('home')
    else:
        form = RequestForm(instance=req)
    context = {
        'form': form, 
        'request': req
    }
    return render(request, 'fleetApp/requisition/edit_request.html', context)

@login_required
def delete_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        req.delete()
        messages.success(request, "Request deleted successfully!")
        return redirect('home')
    context = {
        'request': req
    }
    return render(request, 'fleetApp/requisition/delete_request.html', context)

# List all requests
@login_required
def request_list(request):
    # Get the status filter from the query parameters
    status_filter = request.GET.get('status')
    if status_filter == 'pending':
        requests = Request.objects.filter(request_status='P')  # 'P' for Pending
    elif status_filter == 'closed':
        requests = Request.objects.filter(request_status='C')  # 'C' for Closed
    else:
        requests = Request.objects.all()  

    context = {
        'requests': requests
    }
    return render(request, 'fleetApp/requisition/request_list.html', context)

# Approve a request
@login_required
def approve_request(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        selected_vehicle_id = request.POST.get('vehicle')
        selected_vehicle = get_object_or_404(Vehicle, id=selected_vehicle_id)

        request_obj.vehicle = selected_vehicle
        request_obj.request_status = "O"  # Open (Allocated)
        request_obj.time_of_allocation = timezone.now()
        request_obj.mileage_at_assignment = selected_vehicle.mileage
        request_obj.save()

        # Define the driver assigned to the vehicle
        selected_driver = Driver.objects.filter(vehicle=selected_vehicle).first()
        request_obj.driver = selected_driver 
        request_obj.save()

        # Notify Driver
        if selected_driver:
            send_notification(
                subject='Vehicle Assigned for Trip',
                template_name='emails/trip_assigned_driver.html',
                context={
                    'driver_name': selected_driver.driver_name,
                    'vehicle': selected_vehicle.vehicle_plate,
                    'destination': request_obj.destination,
                    'date': request_obj.time_of_allocation.date(),
                    'time': request_obj.time_of_allocation.time()
                },
                recipient_email=selected_driver.email_address
            )

        # Notify Requestor
        send_notification(
            subject='Trip Approved',
            template_name='emails/trip_approved_requestor.html',
            context={
                'requestor_name': request_obj.requestor.username,
                'vehicle': selected_vehicle.vehicle_plate,
                'driver': selected_driver.driver_name if selected_driver else "Not Assigned",
                'driver_contact': selected_driver.contact if selected_driver else "N/A"
            },
            recipient_email=request_obj.requestor.email
        )

        selected_vehicle.status = "Al"  # Allocated
        selected_vehicle.save()

        messages.success(request, "Request approved successfully!")
        return redirect('requisitions')
    return redirect('requisitions')

@login_required
def request_summary(request):
    # All closed requests
    closed_requests = Request.objects.filter(request_status="C")

    # Annotate usage (mileage used) for trip summary
    trip_summary = closed_requests.annotate(
        usage_summary=ExpressionWrapper(
            F('mileage_at_return') - F('mileage_at_assignment'),
            output_field=IntegerField()
        )
    )

    return render(request, "fleetApp/requisition/request_summary.html", {
        "closed_requests": closed_requests,
        "trip_summary": trip_summary
    })

#######################################################################################################################################
######################################## This Section for Service Provider Views #######################################################

@login_required
def add_service_provider(request):
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service provider added successfully!")
            return redirect('service_provider_list')
        else:
            messages.error(request, "Failed to add service provider. Please check the form.")
    else:
        form = ServiceProviderForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/serviceProvider/add_service_provider.html', context)

# ServiceProvider Views
@login_required
def service_provider_list(request):
    providers = ServiceProvider.objects.all()
    context = {'providers': providers}
    return render(request, 'fleetApp/serviceProvider/service_providers.html', context)


@login_required
def edit_service_provider(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            messages.success(request, "Service provider updated successfully!")
            return redirect('service_provider_list')
        else:
            messages.error(request, "Failed to update service provider. Please check the form.")
    else:
        form = ServiceProviderForm(instance=provider)
    context = {
        'form': form, 
        'provider': provider
    }
    return render(request, 'fleetApp/serviceProvider/edit_service_provider.html', context)


@login_required
def delete_service_provider(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    if request.method == 'POST':
        provider.delete()
        messages.success(request, "Service provider deleted successfully!")
        return redirect('service_provider_list')
    
    context = {
        'provider': provider
    }
    return render(request, 'fleetApp/serviceProvider/delete_service_provider.html', context)

#####################################################################################################################
######################################## SECTION FOR Service Views ##################################################

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully!")
            return redirect('service_list')
        else:
            messages.error(request, "Failed to add service. Please check the form.")
    else:
        form = ServiceForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/service/add_service.html', context)

@login_required
def service_list(request):
    services = Service.objects.select_related('vehicle', 'service_provider').all()
    context = {
        'services': services
    }
    return render(request, 'fleetApp/service/services.html', context)

@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect('service_list')
        else:
            messages.error(request, "Failed to update service. Please check the form.")
    else:
        form = ServiceForm(instance=service)
    context = {
        'form': form, 
        'service': service
    }
    return render(request, 'fleetApp/service/edit_service.html', context)

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect('service_list')
    
    context = {
        'service': service
    }
    return render(request, 'fleetApp/service/delete_service.html', context)

####################################################################################################
##################################### GSM & ALERT VIEW SECTION ##########################################

# GSM Sensor Data
@login_required
def gsm_data_list(request):
    data = GSMsensorData.objects.all().order_by('-timestamp')
    return render(request, 'fleetApp/gsm/gsm_data_list.html', {'data': data})

@login_required
def add_gsm_data(request):
    if request.method == 'POST':
        form = GSMsensorDataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sensor data recorded successfully.')
            return redirect('gsm_data_list')
    else:
        form = GSMsensorDataForm()
    return render(request, 'fleetApp/gsm/add_gsm_data.html', {'form': form})


# Alerts
@login_required
def alert_list(request):
    alerts = Alert.objects.all().order_by('-timestamp')
    return render(request, 'fleetApp/alerts/alert_list.html', {'alerts': alerts})

@login_required
def add_alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alert added successfully.')
            return redirect('alert_list')
    else:
        form = AlertForm()
    return render(request, 'fleetApp/alerts/add_alert.html', {'form': form})

####################################################################################################
##################################### PDF & CSV EXPORTS VIEW SECTION ##########################################

#PDF Export using ReportLab

@login_required
def report_selection_view(request):
    return render(request, 'fleetApp/reports/report_selection.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def report_selection_view(request):
    return render(request, 'fleetApp/reports/report_selection.html')

@login_required
def generate_report_view(request):
    report_type = request.GET.get("report_type")

    if report_type == "closed_trips":
        return redirect('export_trip_logs_pdf')  # or another view
    elif report_type == "assigned_trips":
        return redirect('report_assigned_trips')
    elif report_type == "vehicle_mileage":
        return redirect('report_vehicle_mileage')
    elif report_type == "vehicle_info":
        return redirect('report_all_vehicles')
    elif report_type == "serviced_vehicles":
        return redirect('report_serviced_vehicles')
    elif report_type == "available_vehicles":
        return redirect('report_available_vehicles')
    elif report_type == "vehicle_requests":
        return redirect('report_vehicle_requests')
    elif report_type == "closure_rate":
        return redirect('report_closure_rate')
    else:
        return redirect('report_selection')
  
  

# === REPORT 1: Assigned Trips ===
@login_required
def report_assigned_trips(request):
    trips = Request.objects.filter(vehicle__isnull=False)
    return render(request, 'fleetApp/reports/assigned_trips.html', {'trips': trips})

@login_required
def export_assigned_trips_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assigned_trips.csv"'
    writer = csv.writer(response)
    writer.writerow(['Requestor', 'Vehicle', 'Driver', 'Destination'])
    for trip in Request.objects.filter(vehicle__isnull=False):
        driver = trip.driver.driver_name if trip.driver else 'N/A'
        writer.writerow([trip.requestor.username, trip.vehicle.vehicle_plate, driver, trip.destination])
    return response

# === REPORT 2: Vehicle Mileage ===
@login_required
def report_vehicle_mileage(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'fleetApp/reports/vehicle_mileage.html', {'vehicles': vehicles})

# === REPORT 3: All Vehicle Information ===
@login_required
def report_all_vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'fleetApp/reports/all_vehicles.html', {'vehicles': vehicles})

# === REPORT 4: Serviced Vehicles ===
@login_required
def report_serviced_vehicles(request):
    services = Service.objects.select_related('vehicle').order_by('-service_date')
    return render(request, 'fleetApp/reports/serviced_vehicles.html', {'services': services})

# === REPORT 5: Available Vehicles ===
@login_required
def report_available_vehicles(request):
    assigned_vehicles = Request.objects.filter(request_status__in=['P', 'O']).values_list('vehicle_id', flat=True)
    available = Vehicle.objects.exclude(id__in=assigned_vehicles)
    return render(request, 'fleetApp/reports/available_vehicles.html', {'vehicles': available})

# === REPORT 6: All Vehicle Requests ===
@login_required
def report_vehicle_requests(request):
    requests = Request.objects.all().order_by('-request_date')
    return render(request, 'fleetApp/reports/vehicle_requests.html', {'requests': requests})

# === REPORT 7: Closure Rate ===
@login_required
def report_closure_rate(request):
    total_requests = Request.objects.count()
    closed_requests = Request.objects.filter(request_status='C').count()
    rate = (closed_requests / total_requests * 100) if total_requests > 0 else 0
    return render(request, 'fleetApp/reports/closure_rate.html', {
        'total': total_requests,
        'closed': closed_requests,
        'rate': round(rate, 2),
    })

@login_required
def export_trip_logs_pdf(request):
    closed_trips = Request.objects.filter(request_status='C')
    template_path = 'fleetApp/reports/closed_trips_pdf.html'  # Make sure this template exists
    context = {'trips': closed_trips}

    # Render HTML to PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="closed_trips.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF generation failed: %s' % pisa_status.err)
    return response

# CSV Export: Trip Logs with Alerts

@login_required
def export_trip_logs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="closed_trips.csv"'

    writer = csv.writer(response)
    writer.writerow(['Requestor', 'Vehicle', 'Driver', 'Destination', 'Status', 'Request Date'])

    closed_trips = Request.objects.filter(request_status='C')
    for trip in closed_trips:
        driver = trip.driver.driver_name if trip.driver else 'N/A'
        writer.writerow([
            trip.requestor.username,
            trip.vehicle.vehicle_plate if trip.vehicle else 'N/A',
            driver,
            trip.destination,
            trip.request_status,
            trip.request_date.strftime('%Y-%m-%d')
        ])
    return response

@login_required
def export_vehicle_mileage_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vehicle_mileage.csv"'
    writer = csv.writer(response)
    writer.writerow(['Vehicle Plate', 'Current Mileage'])

    for vehicle in Vehicle.objects.all():
        writer.writerow([vehicle.vehicle_plate, vehicle.mileage])
    return response

@login_required
def export_all_vehicles_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_vehicles.csv"'
    writer = csv.writer(response)
    writer.writerow(['Vehicle Plate', 'Model', 'Make', 'Year', 'Mileage', 'Status'])

    for v in Vehicle.objects.all():
        writer.writerow([v.vehicle_plate, v.model, v.make, v.year, v.mileage, v.status])
    return response

@login_required
def export_serviced_vehicles_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="serviced_vehicles.csv"'
    writer = csv.writer(response)
    writer.writerow(['Vehicle Plate', 'Service Type', 'Service Date', 'Cost'])

    for record in ServiceRecord.objects.select_related('vehicle').order_by('-service_date'):
        writer.writerow([
            record.vehicle.vehicle_plate,
            record.service_type,
            record.service_date.strftime('%Y-%m-%d'),
            record.service_cost
        ])
    return response

@login_required
def export_available_vehicles_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="available_vehicles.csv"'
    writer = csv.writer(response)
    writer.writerow(['Vehicle Plate', 'Model', 'Make', 'Year'])

    assigned_ids = Request.objects.filter(request_status__in=['P', 'O']).values_list('vehicle_id', flat=True)
    available = Vehicle.objects.exclude(id__in=assigned_ids)

    for vehicle in available:
        writer.writerow([vehicle.vehicle_plate, vehicle.model, vehicle.make, vehicle.year])
    return response
 
@login_required
def export_vehicle_requests_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vehicle_requests.csv"'
    writer = csv.writer(response)
    writer.writerow(['Requestor', 'Destination', 'Vehicle', 'Driver', 'Status', 'Request Date'])

    for r in Request.objects.all().order_by('-request_date'):
        writer.writerow([
            r.requestor.username,
            r.destination,
            r.vehicle.vehicle_plate if r.vehicle else 'N/A',
            r.driver.driver_name if r.driver else 'N/A',
            r.request_status,
            r.request_date.strftime('%Y-%m-%d')
        ])
    return response

@login_required
def export_closure_rate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="closure_rate.csv"'
    writer = csv.writer(response)
    writer.writerow(['Total Requests', 'Closed Requests', 'Closure Rate (%)'])

    total = Request.objects.count()
    closed = Request.objects.filter(request_status='C').count()
    rate = (closed / total * 100) if total > 0 else 0

    writer.writerow([total, closed, round(rate, 2)])
    return response

  
#Trip Views
@login_required
def trip_history(request):
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        messages.error(request, "No driver profile found for this user.")
        return redirect('home')

    trips = Request.objects.filter(
        driver=driver,
        request_status='C'
    ).select_related('vehicle', 'requestor')

    for trip in trips:
        trip.mileage_used = (
            (trip.mileage_at_return or 0) - (trip.mileage_at_assignment or 0)
        )

    return render(request, 'fleetApp/driver/trip_history.html', {'trips': trips})


@login_required
def assigned_trips(request):
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        messages.error(request, "No driver profile found for this user.")
        return redirect('home')

    # Only get requests that are still open (assigned)
    trips = Request.objects.filter(
        vehicle=driver.vehicle,
        request_status='O'
    ).select_related('vehicle', 'requestor')

    return render(request, 'fleetApp/driver/assigned_trips.html', {'trips': trips})

