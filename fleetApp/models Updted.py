from django.db import models
from django.utils import timezone

# VEHICLE
class Vehicle(models.Model):
    ENGINE_CHOICES = [
        ("GAS", "Gasoline"),
        ("HYB", "Hybrid"),
        ("DIS", "Diesel"),
        ("ELE", "Electric"),
    ]
    STATUS_CHOICES = [
        ("AV", "Available"),
        ("AL", "Allocated"),
        ("UM", "Under Maintenance"),
        ("OS", "Out of Service"),
    ]

    vehicle_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()
    engine_type = models.CharField(max_length=4, choices=ENGINE_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="AV")

    def __str__(self):
        return f"{self.vehicle_plate} - {self.vehicle_type} ({self.status})"

    def return_vehicle(self):
        self.status = 'AV'
        self.save()


# DRIVER
class Driver(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    driver_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=20)
    email_address = models.EmailField(unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.driver_name} ({self.contact})"


# STAFF (Replaces Requestor + Request)
class Staff(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    email_address = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class VehicleRequest(models.Model):
    STATUS_CHOICES = [
        ("P", "Pending"),
        ("A", "Approved"),
        ("R", "Rejected"),
        ("C", "Completed"),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    purpose = models.CharField(max_length=100)
    current_location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    time_of_allocation = models.DateTimeField(null=True, blank=True)
    mileage_at_assignment = models.IntegerField(null=True, blank=True)
    mileage_at_return = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Request by {self.staff.name} on {self.request_date}"

    def allocate(self, vehicle, driver):
        self.vehicle = vehicle
        self.driver = driver
        self.time_of_allocation = timezone.now()
        self.status = "A"
        self.mileage_at_assignment = vehicle.mileage
        self.save()

    def close_request(self, mileage_returned):
        self.mileage_at_return = mileage_returned
        self.status = "C"
        self.save()

    def get_distance_covered(self):
        if self.mileage_at_assignment and self.mileage_at_return:
            return self.mileage_at_return - self.mileage_at_assignment
        return 0


# SERVICE PROVIDER
class ServiceProvider(models.Model):
    service_provider_name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    email_address = models.EmailField(unique=True)

    def __str__(self):
        return self.service_provider_name


# SERVICE
class Service(models.Model):
    particular = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.particular} for {self.vehicle.vehicle_plate}"

    def total_cost(self):
        return self.quantity * self.cost


# GSM SENSOR DATA
class GSMSensorData(models.Model):
    SENSOR_TYPE_CHOICES = [
        ("FUEL", "Fuel Level"),
        ("SPD", "Speed"),
        ("ENG", "Engine Status"),
        ("MIL", "Mileage"),
        ("GPS", "Location"),
    ]
    TRANSMISSION_MODES = [
        ("SMS", "SMS"),
        ("GPRS", "GPRS"),
        ("EMAIL", "Email"),
        ("NOTIFY", "In-App Notification"),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=10, choices=SENSOR_TYPE_CHOICES)
    data_value = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    transmission_mode = models.CharField(max_length=10, choices=TRANSMISSION_MODES)

    def __str__(self):
        return f"{self.sensor_type} reading for {self.vehicle.vehicle_plate}"


# ALERTS
class Alert(models.Model):
    PRIORITY_CHOICES = [
        ("HIGH", "High"),
        ("MED", "Medium"),
        ("LOW", "Low"),
    ]
    RECIPIENT_ROLES = [
        ("FLEET_MANAGER", "Fleet Manager"),
        ("DRIVER", "Driver"),
        ("BOTH", "Both"),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sensor_data = models.ForeignKey(GSMSensorData, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50)
    alert_message = models.CharField(max_length=255)
    trigger_source = models.CharField(max_length=50)
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    recipient_role = models.CharField(max_length=20, choices=RECIPIENT_ROLES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type} Alert - {self.vehicle.vehicle_plate}"
