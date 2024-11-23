from django.urls import path
from . import views

urlpatterns = [
         # Main view
   # path('', views.main_view, name='main'),
    
         # Home urls
    path('', views.home_view, name='home'),
    
         ############################################################################# Vehicle urls ###########################
    path('vehicles/', views.vehicle_view, name='vehicle'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'), 
    path('edit-vehicle/<int:vehicle_id>/', views.vehicle_update, name='edit_vehicle'),
    path('delete-vehicle/<int:vehicle_id>/', views.vehicle_delete, name='delete_vehicle'),
    path('allocate-vehicle/<int:vehicle_id>/', views.allocate_vehicle, name='allocate_vehicle'),
    path('return_vehicle/<int:vehicle_id>/', views.return_vehicle, name='return_vehicle'),


#################################################################### Driver urls
     path('drivers/', views.drivers_list, name='drivers'),
     path('drivers/add/', views.add_driver, name='add_driver'),
     path('drivers/edit/<int:driver_id>/', views.edit_driver, name='edit_driver'),
     path('drivers/delete/<int:driver_id>/', views.delete_driver, name='delete_driver'),
     
################################################################### Service Provider urls
     path('service-providers/', views.service_provider_list, name='service_provider_list'),
     path('service-providers/add/', views.add_service_provider, name='add_service_provider'),
     path('service-providers/edit/<int:provider_id>/', views.edit_service_provider, name='edit_service_provider'),
     path('service-providers/delete/<int:provider_id>/', views.delete_service_provider, name='delete_service_provider'),
     
 #################################################################### Service URLs
     path('services/', views.service_list, name='service_list'),
     path('services/add/', views.add_service, name='add_service'),
     path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
     path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
]
