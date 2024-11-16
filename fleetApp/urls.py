from django.urls import path
from . import views

urlpatterns = [
         # Main view
    path('', views.main_view, name='main'),
    
         # Home view
    path('home/', views.home_view, name='home'),
    
         # Vehicle view
    path('vehicles/', views.vehicle_view, name='vehicle'),
    
    # Add new vehicle
    path('add-vehicle/', views.add_vehicle, name='add_vehicle')
]