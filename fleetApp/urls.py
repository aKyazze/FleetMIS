from django.urls import path
from . import views

urlpatterns = [
         # Main view
    path('', views.main_view, name='main'),
    
         # Home urls
    path('home/', views.home_view, name='home'),
    
         # Vehicle urls
    path('vehicles/', views.vehicle_view, name='vehicle'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'), 
    path('edit-vehicle/<int:vehicle_id>/', views.vehicle_update, name='edit_vehicle'),
    path('delete-vehicle/<int:vehicle_id>/', views.vehicle_delete, name='delete_vehicle'),
    path('allocate-vehicle/<int:vehicle_id>/', views.allocate_vehicle, name='allocate_vehicle'),

]
