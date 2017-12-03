from django.db import models
from datetime import date

# Creating enquiry model.
class Enquiry(models.Model):
    """Create enquiries that are in Quote Retrieval stage or have
    been finalised"""
    # Defining choices for status and load type fields.
    # Status choice fields
    QuoteRequired = 'QR'
    FinalisedOrder = 'FO'
    status_choices = (
        (QuoteRequired, 'Quote Required'),
        (FinalisedOrder, 'Finalised Order'),
    )
    # Load type choice fields
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

    # Defining model fields
    enquiry_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=2, choices=status_choices,
                              default=QuoteRequired, blank=False)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    return_location = models.CharField(max_length=255, blank=True, null=True)
    # Since vehicle_type and vehicle_body may be required to alter from admin
    # panel for multiple times in the future, we are defining them as seperate
    # models and using ForeignKey to connect the models in many to one
    # relationship.
    vehicle_type = models.ManyToManyField('masters.Vehicle_type')
    vehicle_body = models.ManyToManyField('masters.Vehicle_body', blank=True)
    load_type = models.CharField(max_length=3, choices=load_type_choices,
                                 default=Normal, blank=False)
    special_req = models.TextField(blank=True, null=True)
    deal_number = models.PositiveIntegerField(blank=True, null=True)
    loading_date = models.DateField(default=date.today)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Deal No:%s - %s to %s' %(self.deal_number,self.source,self.destination)

class SupplierQuote(models.Model):
    quote_id = models.AutoField(primary_key=True)
    enquiry = models.ForeignKey('Enquiry', blank=False, null=True,
                                on_delete=models.SET_NULL)
    transporter = models.ForeignKey('masters.Transporter', blank=False,
                                    null=True, on_delete=models.SET_NULL)
    rate = models.PositiveIntegerField(blank=False, null=False)
    including_fine = models.BooleanField()
    vehicle_avail = models.BooleanField()
    vehicle_type = models.ManyToManyField('masters.vehicle_type')
    