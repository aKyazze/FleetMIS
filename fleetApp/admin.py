from django.contrib import admin
from .models import Vehicle, Driver, Requisition, ServiceProvider, Service

# Register your models here.


admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Requisition)
admin.site.register(ServiceProvider)
admin.site.register(Service)