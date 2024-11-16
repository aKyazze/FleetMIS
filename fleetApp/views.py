from django.shortcuts import render, redirect
from .models import Vehicle, Driver
from .forms import VehicleForm

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

# Create or Add a New Vehicle
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle')
    else:
        form = VehicleForm()
    return render(request, 'fleetApp/vehicle/add_vehicle.html', {'form': form})


