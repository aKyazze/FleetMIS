from django.shortcuts import render, redirect, get_object_or_404
#from django.utils.timezone import now
from django.utils import timezone 
from django.db.models import F, ExpressionWrapper, IntegerField
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Vehicle, Driver, Requestor, Request, ServiceProvider, Service
#, GSMsensorData, Alert
from .forms import VehicleForm, VehicleAllocationForm, DriverForm, ServiceProviderForm, ServiceForm, RequestorForm, RequestForm, RequestApprovalForm, VehicleReturnForm
#, SensorDataForm, AlertForm


MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
# Create your views here.
############################################################################################
######################### LOGIN VIEWSS #####################################################
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

#This is API endpoint view to return user Details by ID
@require_GET
@login_required
def get_user_info(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'name': f"{user.first_name} {user.last_name}".strip(),
            'email': user.email,
            # Assume contact is stored in user.profile or skip it if not available
            'contact': user.profile.contact if hasattr(user, 'profile') else '',
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
####################################################################################################
##################################### MAIN & HOME SECTION ##########################################

#This is the Main view
@login_required
def main_view(request):
    return render(request, 'main.html')

#This is Home View
@login_required
def home_view(request):
    # Get statistics for the dashboard
    total_vehicles = Vehicle.objects.count()
    total_drivers = Driver.objects.count()
    total_pending_requests = Request.objects.filter(request_status="P").count()
    total_completed_requests = Request.objects.filter(request_status="C").count()
    total_services = Service.objects.count()
    total_requestors = Requestor.objects.count()
    total_service_providers = ServiceProvider.objects.count()

    context = {
        'total_vehicles': total_vehicles,
        'total_drivers': total_drivers,
        'total_pending_requests': total_pending_requests,
        'total_completed_requests': total_completed_requests,
        'total_services': total_services,
        'total_requestors': total_requestors,
        'total_service_providers': total_service_providers, 
    }
    return render(request, 'fleetApp/base/home.html', context)

####################################################################################################
##################################### STAFF VIEWS SECTION ##########################################
# Staff
@login_required
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'fleetmisApp/staff_form.html', {'form': form})

@login_required
def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'fleetmisApp/staff_list.html', {'staff': staff})

@login_required
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'fleetmisApp/staff_form.html', {'form': form})

@login_required
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'fleetmisApp/staff_confirm_delete.html', {'staff': staff})


############################################################################################################
##################################### FLEET MANAGER VIEWS SECTION ##########################################

# Fleet Manager
@login_required
def fleet_manager_list(request):
    managers = FleetManager.objects.all()
    return render(request, 'fleetmisApp/fleet_manager_list.html', {'managers': managers})

@login_required
def add_fleet_manager(request):
    if request.method == 'POST':
        form = FleetManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fleet_manager_list')
    else:
        form = FleetManagerForm()
    return render(request, 'fleetmisApp/fleet_manager_form.html', {'form': form})


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
            return redirect('home')
        else:
            messages.error(request, "Failed to add vehicle. Please check the form.")
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
            return redirect('home')
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
        return redirect('home')
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
            return redirect('home')
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
            
            # Update the vehicle and request status
            vehicle.status = 'Available'
            vehicle.mileage = mileage_at_return
            driver = Driver.objects.filter(vehicle=vehicle).first()
            if driver:
                driver.vehicle = None
                driver.save()

            request_obj = Request.objects.filter(vehicle=vehicle, request_status="O").first()
            if request_obj:
                request_obj.close_request(mileage_at_return)
                request_obj.mileage_at_return = mileage_at_return
                request_obj.request_status = "C"
                request_obj.save()

            vehicle.save()

            messages.success(request, "Vehicle returned successfully!")
            return redirect('home')
        else:
            messages.error(request, "Failed to return vehicle. Please check the form.")
    else:
        form = VehicleReturnForm()

    return render(request, 'fleetApp/vehicle/return_vehicle.html', {'vehicle': vehicle, 'form': form})


#############################################################################################################
######################################## SECTION FOR Driver Views ###########################################

# New Driver View 
@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver added successfully!")
            return redirect('home')
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
    drivers = Driver.objects.select_related('vehicle').all()  # Get drivers with their associated vehicles
    # Loop through drivers to ensure "Unassigned" is shown if no vehicle is assigned
    for driver in drivers:
        if not driver.vehicle:
            driver.vehicle_plate = "Unassigned"  # Set the vehicle_plate to "Unassigned" if no vehicle is assigned
        else:
            driver.vehicle_plate = driver.vehicle.vehicle_plate  # Otherwise, display the vehicle plate
    form = DriverForm()  # Driver form (if needed for adding new drivers)
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
            return redirect('home')
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
        return redirect('home')
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
            return redirect('home')
        else:
            messages.error(request, "Failed to add requestor. Please check the form.")
    else:
        form = RequestorForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/requisition/add_requestor.html', context)

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
            return redirect('home')
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
        return redirect('home')
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
    vehicles = Vehicle.objects.filter(status="Allocated")  # Only allocated vehicles
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
        requestor = request.user.requestor  # Assumes OneToOne relation
    except Requestor.DoesNotExist:
        messages.error(request, "No requestor profile found for this user.")
        return redirect('home')

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            #new_request.requestor = requestor
            new_request.requestor = request.user
            new_request.save()
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
        requests = Request.objects.all()  # Default: show all requests

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

        selected_vehicle.status = "Al"  # Allocated
        selected_vehicle.save()

        messages.success(request, "Request approved successfully!")
        return redirect('requisitions')  # or 'home' as you prefer
    return redirect('requisitions')


from django.db.models import F, ExpressionWrapper, IntegerField

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
            return redirect('home')
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
            return redirect('home')
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
        return redirect('home')
    #else:
     #   messages.error(request, "Failed to delete service provider. Please try again.")
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
            return redirect('home')
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
            return redirect('home')
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
        return redirect('home')
    #else:
        #messages.error(request, "Failed to delete service. Please try again.")
    context = {
        'service': service
    }
    return render(request, 'fleetApp/service/delete_service.html', context)


####################################################################################################
##################################### GSM & ALERT VIEW SECTION ##########################################

# GSM Sensor Data

def sensor_data_list(request):
    data = GSMsensorData.objects.all()
    return render(request, 'fleetmisApp/sensor_data_list.html', {'data': data})

# Alerts

def alert_list(request):
    alerts = Alert.objects.all()
    return render(request, 'fleetmisApp/alert_list.html', {'alerts': alerts})

