from rest_framework import serializers
from .models import Request, Vehicle, Driver

#  Serializer for nested vehicle data
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_plate']

# Serializer for nested driver data
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'driver_name', 'contact']

# Serializer for viewing requests (includes vehicle & driver)
class RequestReadSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Request
        fields = [
            'id',
            'current_location',
            'destination',
            'purpose',
            'request_date',
            'required_date',
            'request_status',
            'vehicle',
            'driver',
        ]

# Serializer for creating requests (same as your original)
class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['current_location', 'destination', 'purpose', 'required_date']
        
class TripSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    requestor = serializers.SerializerMethodField()

    def get_requestor(self, obj):
        return obj.requestor.get_full_name() or obj.requestor.username

    class Meta:
        model = Request
        fields = [
            'id', 'destination', 'purpose', 'request_status',
            'request_date', 'required_date', 'vehicle', 'requestor',
            'mileage_at_assignment', 'mileage_at_return'
        ]

