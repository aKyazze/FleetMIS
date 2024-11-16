from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehicle, Driver
from .forms import VehicleForm, VehicleAllocationForm

# Create your views here.

#This is the Main view

def main_view(request):
    return render(request, 'main.html')

#This is Home View
def home_view(request):
    
    return render(request, 'fleetApp/base/home.html')

# This is Vehicle View
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

            return redirect('vehicle')  # Redirect to vehicle list
    else:
        form = VehicleAllocationForm()

    return render(request, 'fleetApp/vehicle/allocate_vehicle.html', {'form': form, 'vehicle': vehicle})





