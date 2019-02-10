from django.contrib import admin
from .models import VehicleType, VehicleBody, Transporter, ExtraExpenses

# Register your models here.
admin.site.register(VehicleType)
admin.site.register(VehicleBody)
admin.site.register(Transporter)
admin.site.register(ExtraExpenses)
