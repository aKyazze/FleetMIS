from django.db import models

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
    ("Av", "Available"), 
    ("Al", "Allocated")
  ]
 # vehicle_id = models.AutoField(primary_key=True)
  vehicle_plate = models.CharField(max_length=20)
  vehicle_type = models.CharField(max_length=50)
  mileage = models.PositiveIntegerField()
  engine_type = models.CharField(max_length=4, choices=ENGIN)
  status = models.CharField(max_length=2, choices=STATUS, default="Available")
  
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
  #driver_id = models.AutoField(primary_key=True)
  driver_name = models.CharField(max_length=50)
  gender = models.CharField(max_length=2, choices=GENDER_OPTION)
  contact = models.CharField(max_length=20)
  email_address = models.EmailField()
  vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
  
  
  def __str__(self):
      return f"{self.driver_name} {self.contact} {self.vehicle}"
    
#Requisition Entity:
class Requisition(models.Model):
  #requisition_id = models.AutoField(primary_key=True)
  REQUEST_STATE= [
    ("P", "Pending"),
    ("O", "Open"),
    ("C", "Closed")
  ]
  request_date = models.DateField(auto_now=False)
  applicant_name = models.CharField(max_length=50)
  applicant_contact = models.CharField(max_length=20)
  applicant_email = models.EmailField()
  current_location = models.CharField(max_length=50)
  destination = models.CharField(max_length=50)
  purpose = models.CharField(max_length=40)
  time_of_allocation = models.DateTimeField()
  request_status = models.CharField(max_length=3, choices=REQUEST_STATE)
  mileage_at_assignment = models.IntegerField()
  mileage_at_return = models.IntegerField()
  vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
  
  def __str__(self):
    return f"{self.request_date} {self.applicant_name} {self.applicant_contact} {self.current_location} {self.destination}"


#Service Provider Entity:
class ServiceProvider(models.Model):
    #service_provider_id = models.AutoField(primary_key=True)
    service_provider_name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    email_address = models.EmailField()
def __str__(self):
  return f"{self.service_provider_name}"

#Service Entity:
class Service(models.Model):
    #service_id = models.AutoField(primary_key=True)
    particular = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    
    def __str__(self):
      return f"Total Pay {self.quantity}*{self.cost}"
    
    