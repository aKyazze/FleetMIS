# Django imports
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

# Vehicle Entity:
class Vehicle(models.Model):
  ENGIN = [
    ("GAS", "Gasoline"),
    ("HYB", "Hybrid"),
    ("DIS", "Diesel"),
    ("ELE", "Electric")
  ]
  STATUS = [
    ("Available", "Available"), 
    ("Allocated", "Allocated")
  ]
  VEHICLE_TYPE = [
        ("Saloon", "Saloon Car"),
        ("SUV", "SUV (Sport Utility Vehicle)"),
        ("Pickup", "Pickup Truck"),
        ("Truck", "Cargo Truck"),
        ("Motorcycle", "Motorcycle"),
        ("Van", "Van"),
        ("DoubleCab", "Double Cabin"),
  ]
  SERVICE_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
  
  vehicle_plate = models.CharField(max_length=20, unique=True)
  vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE)
  mileage = models.PositiveIntegerField()
  engine_type = models.CharField(max_length=4, choices=ENGIN)
  status = models.CharField(max_length=9, choices=STATUS, default="Available")
  service_status = models.CharField(max_length=20,choices=SERVICE_STATUS_CHOICES,default='PENDING')
  
  def __str__(self):
      return f"{self.vehicle_plate} {self.vehicle_type} ({self.mileage})- {self.status}"
    
  def return_vehicle(self):
      self.status = 'Available'
      self.save()
      
#Driver Entity:
class Driver(models.Model):
  GENDER_OPTION = [
    ("M", "Male"), 
    ("F", "Female")
  ]
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  driver_name = models.CharField(max_length=50)
  gender = models.CharField(max_length=2, choices=GENDER_OPTION)
  contact = models.CharField(max_length=20)
  email_address = models.EmailField()
  vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
  
  
  def __str__(self):
      return f"{self.driver_name} {self.contact} {self.vehicle}"
    
#Requisition Entities:
# Requestor Model
class Requestor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    email_address = models.EmailField()

    def __str__(self):
        return self.name

# Request Model

class Request(models.Model):
    REQUEST_STATE = [
        ("P", "Pending"),
        ("O", "Open"),
        ("C", "Closed"),
    ]

    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests")
    request_date = models.DateField(auto_now_add=True)
    required_date = models.DateField(help_text="Date by which vehicle is required") 
    current_location = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    purpose = models.CharField(max_length=100)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')  
    time_of_allocation = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    request_status = models.CharField(max_length=1, choices=REQUEST_STATE, default="P")
    mileage_at_assignment = models.IntegerField(null=True, blank=True)
    mileage_at_return = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return f"Request by {self.requestor.username} on {self.request_date}"

    def allocate_vehicle(self, vehicle):
        """Assign a vehicle and record mileage at assignment."""
        self.vehicle = vehicle
        self.mileage_at_assignment = vehicle.mileage  # Capture mileage
        self.request_status = "O"  # Set status to Open
        self.time_of_allocation = timezone.now()
        self.save()

    def close_request(self, mileage_at_return):
        """Mark the request as closed and calculate usage."""
        self.mileage_at_return = mileage_at_return
        self.request_status = "C"
       # self.vehicle = None  # Unassign vehicle
        self.save()

    def usage_summary(self):
        """Calculate the usage of the vehicle."""
        if self.mileage_at_assignment is not None and self.mileage_at_return is not None:
            return self.mileage_at_return - self.mileage_at_assignment
        return "N/A"

#Service Provider Entity:
class ServiceProvider(models.Model):
    service_provider_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email_address = models.EmailField()

    def __str__(self):
        return self.service_provider_name
#Service Entity:
class Service(models.Model):
    particular = models.TextField()
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.particular} for {self.vehicle.vehicle_plate}"
    
    def calculate_total(self):
        return self.quantity * self.cost
    
class ServiceFeedback(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    feedback_notes = models.TextField(blank=True)
    invoice_file = models.FileField(upload_to='invoices/')
    submitted_at = models.DateTimeField(auto_now_add=True)


#GSMsensorData Entity: 
class GSMsensorData(models.Model):
    SENSOR_TYPES = [
        ("Speed", "Speed"),
        ("Location", "Location"),
        ("Fuel", "Fuel Level"),
        ("Engine", "Engine Temp"),
    ]
    TRANSMISSION = [
        ("SMS", "SMS"), 
        ("GPRS", "GPRS"), 
        ("USSD", "USSD"), 
        ("Email", "Email"),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    data_value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    transmission_mode = models.CharField(max_length=10, choices=TRANSMISSION)

#Alert Entity:
class Alert(models.Model):
    ALERT_TYPES = [
        ("Low Fuel", "Low Fuel"),
        ("Overspeed", "Overspeeding"),
        ("High Temp", "Engine Overheat"),
    ]
    PRIORITY = [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sensor_data = models.ForeignKey(GSMsensorData, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    alert_message = models.TextField()
    trigger_source = models.CharField(max_length=20)  # 'Sensor Data' or 'Manual'
    priority_level = models.CharField(max_length=10, choices=PRIORITY)
    recipient_role = models.CharField(max_length=50)  # Fleet Manager / Driver
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Staff(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    staff_photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.department})"

class Department(models.Model):
    DEPARTMENT_LIST = [
        ("HR", "Human Resource"), 
        ("IS", "Information System(IT)"), 
        ("FIN", "Finance"), 
        ("COM", "COmmercial"),
        ("FLT", "Fleet")  
    ]
    

    name = models.CharField(max_length=20, choices=DEPARTMENT_LIST)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    contact = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    passport_photo = models.ImageField(upload_to='driver_photos/', null=True, blank=True) 
    department = models.CharField(max_length=20, choices=Department.DEPARTMENT_LIST)


    def __str__(self):
        return f"{self.user.get_full_name()} Profile"
    
