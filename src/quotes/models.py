from django.db import models
from vehicles.models import vehicle_type, vehicle_body
from datetime import date

# Create your models here.
class enquiry(models.Model):
    Enquiry = 'EQ'
    FinalisedOrder = 'FO'
    status_choices = (
        (Enquiry, 'Enquiry'),
        (FinalisedOrder, 'Finalised Order'),
    )
    ODC = 'ODC'
    Normal = 'FTL'
    Part = 'LTL'
    Container = 'CON'
    load_type_choices = (
        (ODC, 'ODC'),
        (Normal, 'Normal'),
        (Part, 'Part'),
        (Container, 'Container'),
    )
    status = models.CharField(max_length=2, choices=status_choices,
                              default=Enquiry, blank=False)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    return_location = models.CharField(max_length=255)
    vehicle_type = models.ForeignKey('vehicles.vehicle_type')
    vehicle_body = models.ForeignKey('vehicles.vehicle_body')
    load_type = models.CharField(max_length=3, choices=load_type_choices,
                                 default=Normal, blank=False)
    special_req = models.TextField()
    deal_number = models.PositiveIntegerField(blank=True, null=True)
    loading_date = models.DateField(default=date.today)
    created = models.DateTimeField(auto_now_add=True)
