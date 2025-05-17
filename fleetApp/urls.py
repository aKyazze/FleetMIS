from django.urls import path
from django.contrib.auth import views as auth_views

from .views import CustomAuthToken
from . import views

urlpatterns = [
         # Main view
   #path('', views.main_view, name='main'),
    
         # Home urls
    path('', views.home_view, name='home'),

    
############################################################################# Vehicle urls 
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
     path('driver/profile/', views.driver_profile_view, name='driver_profile'),

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

##################################################################### Requestor URLs
    path('requestors/', views.requestor_list, name='requestor_list'),
    path('requestors/add/', views.add_requestor, name='add_requestor'),
    path('requestors/edit/<int:requestor_id>/', views.edit_requestor, name='edit_requestor'),
    path('requestors/delete/<int:requestor_id>/', views.delete_requestor, name='delete_requestor'),

    ##################################################################### Request URLs
    path('requisitions/', views.requisitions_view, name='requisitions'),
    path('requestSummary/', views.request_summary, name='request_summary'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/add/', views.add_request, name='add_request'),
    path('requests/edit/<int:request_id>/', views.edit_request, name='edit_request'),
    path('requests/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('requests/delete/<int:request_id>/', views.delete_request, name='delete_request'),
    path('requests/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('my-requests/', views.user_requests, name='user_requests'),
    path('trips/history/', views.trip_history, name='trip_history'),
    path('trips/assigned/', views.assigned_trips, name='assigned_trips'),

    
  #################################################################### API & Registration URLs
   
    path('signUp/', views.sign_up_view, name='registration'),
    path('password/change/', views.custom_password_change, name='password_change'),
    path('password/change/done/', 
         lambda request: render(request, 'registration/password_change_done.html'), 
         name='password_change_done'),
    path('redirect-after-login/', views.login_redirect_view, name='login_redirect'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('api/user-info/', views.get_user_info, name='get_user_info'),
    path('api/login/', CustomAuthToken.as_view(), name='api-login'),
    path('api/fleet/dashboard/', views.fleet_dashboard_api, name='fleet_dashboard_api'),
    path("api/requests/create/", views.create_vehicle_request, name="create_vehicle_request"),
    #path("api/requests/user/", views.user_requests_api, name="user_requests_api"),
    path("api/requests/create/", views.create_vehicle_request, name="create_vehicle_request"),
    path("api/requests/user/", views.get_user_requests, name="get_user_requests"),




  #################################################################### GSMSensor & Alerts URLs
    path('gsm-data/', views.gsm_data_list, name='gsm_data_list'),
    path('gsm-data/add/', views.add_gsm_data, name='add_gsm_data'),
    path('alerts/', views.alert_list, name='alert_list'),
    path('alerts/add/', views.add_alert, name='add_alert'),
    #path('export/trip-logs/csv/', views.export_trip_logs_csv, name='export_trip_logs_csv'),
    #path('export/trip-logs/pdf/', views.export_trip_logs_pdf, name='export_trip_logs_pdf'),
    #path('charts/', views.chart_views, name='chart_views'),
    
    ##################################################################### For Users/Staff
    path('users/register/step1/', views.register_step1, name='register_step1'),
    path('users/register/step2/', views.register_step2, name='register_step2'),
    path('users/', views.user_list, name='user_list'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/<int:user_id>/edit/', views.edit_staff, name='edit_staff'),
    path('staff/<int:user_id>/delete/', views.delete_staff, name='delete_staff'),
    
    ##################################################################### For groups
    path('groups/add/', views.add_group_view, name='add_group'),
    path('groups/', views.group_list_view, name='group_list'),   
    path('groups/<int:group_id>/edit/', views.edit_group_permissions, name='edit_group_permissions'), 
    path('groups/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    
    ##################################################################### For Reports
    
    # Report landing and selector
    path("reports/", views.report_selection_view, name="report_selection"),
    path("reports/generate/", views.generate_report_view, name="generate_report"),

    # PDF and CSV export options
    path("reports/closed_trips/", views.export_trip_logs_pdf, name="export_trip_logs_pdf"),
    path("reports/trip_logs_csv/", views.export_trip_logs_csv, name="export_trip_logs_csv"),

    # Individual report views
    path("reports/assigned_trips/", views.report_assigned_trips, name="report_assigned_trips"),
    path("reports/vehicle_mileage/", views.report_vehicle_mileage, name="report_vehicle_mileage"),
    path("reports/all_vehicles/", views.report_all_vehicles, name="report_all_vehicles"),
    path("reports/serviced/", views.report_serviced_vehicles, name="report_serviced_vehicles"),
    path("reports/available/", views.report_available_vehicles, name="report_available_vehicles"),
    path("reports/requests/", views.report_vehicle_requests, name="report_vehicle_requests"),
    path("reports/closure_rate/", views.report_closure_rate, name="report_closure_rate"),
]


