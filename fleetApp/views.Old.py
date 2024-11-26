from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.db.models import F, ExpressionWrapper, IntegerField
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Vehicle, Driver, Requestor, Request, ServiceProvider, Service
from .forms import VehicleForm, VehicleAllocationForm, DriverForm, ServiceProviderForm, ServiceForm, RequestorForm, RequestForm, RequestApprovalForm, VehicleReturnForm

# Create your views here.
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
    total_pending_requests = Request.objects.filter(request_status="Pending").count()
    total_completed_requests = Request.objects.filter(request_status="Completed").count()
    total_services = Service.objects.count()
    total_requestors = Requestor.objects.count()

    context = {
        'total_vehicles': total_vehicles,
        'total_drivers': total_drivers,
        'total_pending_requests': total_pending_requests,
        'total_completed_requests': total_completed_requests,
        'total_services': total_services,
        'total_requestors': total_requestors,
    }
    return render(request, 'fleetApp/base/home.html', context)

################################### This Section for Vehicle Views ######################################################
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

# Create or Add a New Vehicle View
@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle')
    else:
        form = VehicleForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/vehicle/add_vehicle.html', context)

# Update or Edit Vehicle View
@login_required
def vehicle_update(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
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
        return redirect('vehicle')
    context = {
        'vehicle': vehicle
    }
    return render(request, 'fleetApp/vehicle/vehicle_confirm_delete.html', context)

# Assign or Allocate a Vehicle View 
@login_required
def allocate_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        form = VehicleAllocationForm(request.POST)
        if form.is_valid():
            driver = form.cleaned_data['driver']
            request_instance = form.cleaned_data['request']  # Ensure the request instance is passed

            # Allocate the vehicle to the selected driver
            driver.vehicle = vehicle
            driver.save()

            # Update vehicle status
            vehicle.status = "Allocated"
            vehicle.save()

            # Update request instance with mileage at assignment and allocation time
            request_instance.vehicle = vehicle
            request_instance.mileage_at_assignment = vehicle.mileage  # Capture mileage
            request_instance.time_of_allocation = now()
            request_instance.request_status = "O"  # Mark request as Open
            request_instance.save()

            return redirect('vehicle')
    else:
        form = VehicleAllocationForm()

    context = {
        'form': form,
        'vehicle': vehicle
    }
    return render(request, 'fleetApp/vehicle/allocate_vehicle.html', context)

@login_required
def return_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == "POST":
        form = VehicleReturnForm(request.POST)
        if form.is_valid():
            mileage_at_return = form.cleaned_data['mileage_at_return']
            
            # Update the vehicle and request status
            vehicle.status = 'Available'
            driver = Driver.objects.filter(vehicle=vehicle).first()
            if driver:
                driver.vehicle = None
                driver.save()

            request_obj = Request.objects.filter(vehicle=vehicle, request_status="O").first()
            if request_obj:
                request_obj.close_request(mileage_at_return)

            vehicle.save()
            return redirect('vehicle')
    else:
        form = VehicleReturnForm()

    return render(request, 'fleetApp/vehicle/return_vehicle.html', {'vehicle': vehicle, 'form': form})

######################################## This Section for Driver Views #######################################################
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

# New Driver View 
@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver added successfully!")
            return redirect('drivers')
    else:
        form = DriverForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/driver/add_driver.html', context)

# Driver Update View 
@login_required
def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('drivers')
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
        return redirect('drivers')
    context =  {
        'drivers': driver
    }
    return render(request, 'fleetApp/driver/driver_delete.html', context)

######################################## This Section for Requisition Views #######################################################
# List all requestors
@login_required
def requestor_list(request):
    requestors = Requestor.objects.all()
    context = {
        'requestors': requestors
    }
    return render(request, 'fleetApp/requisition/requestor_list.html', context)

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
        form = RequestorForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/requisition/add_requestor.html', context)

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

@login_required
def edit_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            messages.success(request, "Request updated successfully!")
            return redirect('request_list')
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
        return redirect('request_list')
    context = {
        'request': req
    }
    return render(request, 'fleetApp/requisition/delete_request.html', context)

# List all requests
@login_required
def request_list(request):
    requests = Request.objects.select_related('requestor', 'vehicle').all()
    context = {
        'requests': requests
    }
    return render(request, 'fleetApp/requisition/request_list.html', context)

# Add a new request
@login_required
def add_request(request, requestor_id):
    requestor = get_object_or_404(Requestor, id=requestor_id)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.requestor = requestor
            new_request.save()
            messages.success(request, "Request added successfully!")
            return redirect('request_list')
    else:
        form = RequestForm()
    context = {
        'form': form, 
        'requestor': requestor
    }
    return render(request, 'fleetApp/requisition/add_request.html', context)

# Approve a request
@login_required
def approve_request(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        selected_vehicle_id = request.POST.get('vehicle')
        selected_vehicle = get_object_or_404(Vehicle, id=selected_vehicle_id)

        # Assign the vehicle and update the request
        request_obj.vehicle = selected_vehicle
        request_obj.request_status = "O"  # Open (Allocated)
        request_obj.time_of_allocation
        request_obj.save()

        # Update the vehicle status
        selected_vehicle.status = "Al"  # Allocated
        selected_vehicle.save()

        messages.success(request, "Request approved successfully!")
        return redirect('requisitions')  # Redirect to the fleet management view
    return redirect('requisitions')

@login_required
def fleet_management_view(request):
    requestors = Requestor.objects.all()
    requests = Request.objects.select_related('requestor', 'vehicle').all()
    vehicles = Vehicle.objects.filter(status="Allocated")  # Only allocated vehicles
    requestor_form = RequestorForm()
    context = {
        'requestors': requestors,
        'requests': requests,
        'vehicles': vehicles,
        'requestor_form': requestor_form,
    }
    return render(request, 'fleetApp/requisition/requisitions.html', context)

@login_required
def request_summary(request):
    # Fetch all requests
    requests = Request.objects.all()
    # Pass to the template
    return render(request, "fleetApp/requisition/request_summary.html", {"requests": requests})

######################################## This Section for Service Provider Views #######################################################
# ServiceProvider Views
@login_required
def service_provider_list(request):
    providers = ServiceProvider.objects.all()
    context = {'providers': providers}
    return render(request, 'fleetApp/serviceProvider/service_providers.html', context)

@login_required
def add_service_provider(request):
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_provider_list')
    else:
        form = ServiceProviderForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/serviceProvider/add_service_provider.html', context)

@login_required
def edit_service_provider(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('service_provider_list')
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
        return redirect('service_provider_list')
    context = {
        'provider': provider
    }
    return render(request, 'fleetApp/serviceProvider/delete_service_provider.html', context)

######################################## This Section for Service Views #######################################################
@login_required
def service_list(request):
    services = Service.objects.select_related('vehicle', 'service_provider').all()
    context = {
        'services': services
    }
    return render(request, 'fleetApp/service/services.html', context)

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    context = {
        'form': form
    }
    return render(request, 'fleetApp/service/add_service.html', context)

@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
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
        return redirect('service_list')
    context = {
        'service': service
    }
    return render(request, 'fleetApp/service/delete_service.html', context)

######################################## This Section for Registration Views #######################################################
def sign_up_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            message = "User signed up Successfuly"
        else:
            message = "SignUp Error"
    else:
        form = UserCreationForm
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up.html', context)   






