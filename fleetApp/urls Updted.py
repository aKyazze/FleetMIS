# fleetmisApp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),

    # Staff
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/<int:staff_id>/edit/', views.edit_staff, name='edit_staff'),
    path('staff/<int:staff_id>/delete/', views.delete_staff, name='delete_staff'),

    # Fleet Manager
    path('fleet_managers/', views.fleet_manager_list, name='fleet_manager_list'),
    path('fleet_managers/add/', views.add_fleet_manager, name='add_fleet_manager'),

    # Vehicle
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/<int:vehicle_id>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:vehicle_id>/delete/', views.delete_vehicle, name='delete_vehicle'),

    # Driver
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.add_driver, name='add_driver'),
    path('drivers/<int:driver_id>/edit/', views.edit_driver, name='edit_driver'),
    path('drivers/<int:driver_id>/delete/', views.delete_driver, name='delete_driver'),

    # Service Provider
    path('service_providers/', views.service_provider_list, name='service_provider_list'),
    path('service_providers/add/', views.add_service_provider, name='add_service_provider'),

    # Service / Maintenance
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.add_service, name='add_service'),

    # Alerts
    path('alerts/', views.alert_list, name='alert_list'),

    # GSM Sensor Data
    path('sensor_data/', views.sensor_data_list, name='sensor_data_list'),
]
