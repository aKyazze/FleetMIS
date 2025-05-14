
# This is the Original version
from django.contrib import admin
from .models import Alert, Driver, GSMsensorData, Request, Requestor, Service, ServiceProvider, Staff, Vehicle

# Register your models here.


admin.site.register(Alert)
admin.site.register(Driver)
admin.site.register(GSMsensorData)
admin.site.register(Request)
admin.site.register(Requestor)
admin.site.register(Service)
admin.site.register(ServiceProvider)
admin.site.register(Staff)
admin.site.register(Vehicle)


