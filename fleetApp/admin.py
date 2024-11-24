from django.contrib import admin
from .models import Vehicle, Driver, Requestor, Request, ServiceProvider, Service

# Register your models here.


admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Requestor)
admin.site.register(Request)
admin.site.register(ServiceProvider)
admin.site.register(Service)