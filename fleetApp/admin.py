
# This is the Original version

from django.contrib import admin
from .models import Vehicle, Driver, Requestor, Request, ServiceProvider, Service

# Register your models here.


admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Requestor)
admin.site.register(Request)
admin.site.register(ServiceProvider)
admin.site.register(Service)
'''
from django.contrib import admin
from .models import Vehicle, Driver, Staff, ServiceProvider, Service, GSMsensorData, Alert

admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Staff)
admin.site.register(ServiceProvider)
admin.site.register(Service)
admin.site.register(GSMsensorData)
admin.site.register(Alert)
'''
