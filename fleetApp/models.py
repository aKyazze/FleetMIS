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
    
#Requisition Entities:
# Requestor Model
class Requestor(models.Model):
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
    requestor = models.ForeignKey(Requestor, on_delete=models.CASCADE, related_name="requests")
    request_date = models.DateField(auto_now_add=True)
    current_location = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    purpose = models.CharField(max_length=100)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, null=True, blank=True)
    time_of_allocation = models.DateTimeField(null=True, blank=True)
    request_status = models.CharField(max_length=1, choices=REQUEST_STATE, default="P")
    mileage_at_assignment = models.IntegerField(null=True, blank=True)
    mileage_at_return = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Request by {self.requestor.name} on {self.request_date}"

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
        self.vehicle = None  # Unassign vehicle
        self.save()

    def usage_summary(self):
        """Calculate the usage of the vehicle."""
        if self.mileage_at_assignment and self.mileage_at_return:
            return self.mileage_at_return - self.mileage_at_assignment
        return None


#Service Provider Entity:
class ServiceProvider(models.Model):
    service_provider_name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    email_address = models.EmailField()

    def __str__(self):
        return self.service_provider_name
#Service Entity:
class Service(models.Model):
    particular = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.particular} for {self.vehicle.vehicle_plate}"
    
    def calculate_total(self):
        return self.quantity * self.cost
    
    