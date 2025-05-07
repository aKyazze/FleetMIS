from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff, FleetManager, Vehicle, Driver, ServiceProvider, Service, GSMsensorData, Alert
from .forms import StaffForm, FleetManagerForm, VehicleForm, DriverForm, ServiceProviderForm, ServiceForm, SensorDataForm, AlertForm

# Login and Home

def login_view(request):
    return render(request, 'fleetmisApp/login.html')

def home(request):
    return render(request, 'fleetmisApp/home.html')

# Staff

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'fleetmisApp/staff_form.html', {'form': form})

def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'fleetmisApp/staff_list.html', {'staff': staff})

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

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'fleetmisApp/staff_confirm_delete.html', {'staff': staff})

# Fleet Manager

def fleet_manager_list(request):
    managers = FleetManager.objects.all()
    return render(request, 'fleetmisApp/fleet_manager_list.html', {'managers': managers})

def add_fleet_manager(request):
    if request.method == 'POST':
        form = FleetManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fleet_manager_list')
    else:
        form = FleetManagerForm()
    return render(request, 'fleetmisApp/fleet_manager_form.html', {'form': form})

# Vehicle

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'fleetmisApp/vehicle_list.html', {'vehicles': vehicles})

def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'fleetmisApp/vehicle_form.html', {'form': form})

def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'fleetmisApp/vehicle_form.html', {'form': form})

def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'fleetmisApp/vehicle_confirm_delete.html', {'vehicle': vehicle})

# Driver

def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'fleetmisApp/driver_list.html', {'drivers': drivers})

def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm()
    return render(request, 'fleetmisApp/driver_form.html', {'form': form})

def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'fleetmisApp/driver_form.html', {'form': form})

def delete_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    return render(request, 'fleetmisApp/driver_confirm_delete.html', {'driver': driver})

# Service Provider

def service_provider_list(request):
    providers = ServiceProvider.objects.all()
    return render(request, 'fleetmisApp/service_provider_list.html', {'providers': providers})

def add_service_provider(request):
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_provider_list')
    else:
        form = ServiceProviderForm()
    return render(request, 'fleetmisApp/service_provider_form.html', {'form': form})

# Service

def service_list(request):
    services = Service.objects.all()
    return render(request, 'fleetmisApp/service_list.html', {'services': services})

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'fleetmisApp/service_form.html', {'form': form})

# GSM Sensor Data

def sensor_data_list(request):
    data = GSMsensorData.objects.all()
    return render(request, 'fleetmisApp/sensor_data_list.html', {'data': data})

# Alerts

def alert_list(request):
    alerts = Alert.objects.all()
    return render(request, 'fleetmisApp/alert_list.html', {'alerts': alerts})

