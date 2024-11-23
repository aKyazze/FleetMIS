from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehicle, Driver, ServiceProvider, Service
from .forms import VehicleForm, VehicleAllocationForm, DriverForm, ServiceProviderForm, ServiceForm

# Create your views here.

#This is the Main view
def main_view(request):
    return render(request, 'main.html')

#This is Home View
def home_view(request):
    return render(request, 'fleetApp/base/home.html')

################################### This Section for Vehicle Views ######################################################
def vehicle_view(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles
    }
    return render(request, 'fleetApp/vehicle/vehicles.html', context)

# Create or Add a New Vehicle View
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

            return redirect('vehicle') 
    else:
        form = VehicleAllocationForm()
        
    context = {
        'form': form, 
        'vehicle': vehicle
    }
    return render(request, 'fleetApp/vehicle/allocate_vehicle.html', context)

# Return a Vehicle View 
def return_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    vehicle.status = 'Available'  # Update the vehicle status to "Available"
    # Get the driver associated with the vehicle (if any)
    driver = Driver.objects.filter(vehicle=vehicle).first()  # Find the driver with the given vehicle
    if driver:
        driver.vehicle = None  # Clear the vehicle assignment for the driver
        driver.save()  # Save the driver with the updated vehicle assignment
    vehicle.save()  # Save the vehicle status
    return redirect('vehicle')

######################################## This Section for Driver Views #######################################################

# Driver List View 
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



######################################## This Section for Service Provider Views #######################################################

# ServiceProvider Views
def service_provider_list(request):
    providers = ServiceProvider.objects.all()
    context = {'providers': providers}
    return render(request, 'fleetApp/serviceProvider/service_providers.html', context)

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
def service_list(request):
    services = Service.objects.select_related('vehicle', 'service_provider').all()
    context = {
        'services': services
    }
    return render(request, 'fleetApp/service/services.html', context)

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

def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    context = {
        'service': service
    }
    return render(request, 'fleetApp/service/delete_service.html', context)




