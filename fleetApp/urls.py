from django.urls import path
from . import views

urlpatterns = [
         # Main view
   path('', views.main_view, name='main'),
    
         # Home urls
    path('home/', views.home_view, name='home'),
    
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

# Requestor URLs
    path('requestors/', views.requestor_list, name='requestor_list'),
    path('requestors/add/', views.add_requestor, name='add_requestor'),
    path('requestors/edit/<int:requestor_id>/', views.edit_requestor, name='edit_requestor'),
    path('requestors/delete/<int:requestor_id>/', views.delete_requestor, name='delete_requestor'),

    # Request URLs
    path('requisitions/', views.fleet_management_view, name='requisitions'),
    path('requestSummary/', views.request_summary, name='requestSummary'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/add/<int:requestor_id>/', views.add_request, name='add_request'),
    path('requests/edit/<int:request_id>/', views.edit_request, name='edit_request'),
    path('requests/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('requests/delete/<int:request_id>/', views.delete_request, name='delete_request'),
    
    
  #################################################################### Registration URLs
   
  path('signUp/', views.sign_up_view, name='registration'),
  
    
]


