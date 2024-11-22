from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehicle, Driver
from .forms import VehicleForm, VehicleAllocationForm, DriverForm

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
    return render(request, 'fleetApp/vehicle/vehicles.html', {'vehicles': vehicles})

# Create or Add a New Vehicle View
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle')
    else:
        form = VehicleForm()
    return render(request, 'fleetApp/vehicle/add_vehicle.html', {'form': form})

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
    return render(request, 'fleetApp/vehicle/edit_vehicle.html', {'form': form, 'vehicle': vehicle})


# Delete Vehicle View 
def vehicle_delete(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle')
    return render(request, 'fleetApp/vehicle/vehicle_confirm_delete.html', {'vehicle': vehicle})

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

    return render(request, 'fleetApp/vehicle/allocate_vehicle.html', {'form': form, 'vehicle': vehicle})

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
    return render(request, 'fleetApp/driver/drivers.html', {'drivers': drivers, 'form': form})

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
    return render(request, 'fleetApp/driver/add_driver.html', {'form': form})


# Driver Updtte View 

def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver updated successfully!")
            return redirect('drivers')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'fleetApp/driver/edit_driver.html', {'form': form, 'driver': driver})


# Driver Removing View 

def delete_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        driver.delete()
        return redirect('drivers')
    return render(request, 'fleetApp/driver/driver_delete.html', {'drivers': driver})


######################################## This Section for Requisition Views #######################################################




