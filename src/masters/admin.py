from django.contrib import admin
from .models import Vehicle_type, Vehicle_body, Transporter

# Register your models here.
admin.site.register(Vehicle_type)
admin.site.register(Vehicle_body)
admin.site.register(Transporter)