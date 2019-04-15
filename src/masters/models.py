"""
Models for the Masters Module. This Module has all the masters data which is
used as foreignkeys in other forms.
"""

from django.db import models

# Create your models here.
class VehicleType(models.Model):
    """
    Defining vehicle types like 40' High Bed 20T, 40' Low Bed 20T
    etc.
    """
    vehicle_type_id = models.AutoField(primary_key=True)
    vehicle = models.CharField(max_length=20, blank=False, null=False)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.vehicle

class VehicleBody(models.Model):
    """Defining vehicle body type like half body, full body, open body
     etc."""
    vehicle_body_id = models.AutoField(primary_key=True)
    body = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.body

class Transporter(models.Model):
    """Add and Edit Transporter Details"""
    transporter_id = models.AutoField(primary_key=True)
    transporter = models.CharField(max_length=70, blank=False, null=False)
    primary_mobile = models.PositiveIntegerField(blank=False, null=False)
    primary_person = models.CharField(max_length=40, blank=True, null=True)
    other_contact = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.transporter

class ExtraExpenses(models.Model):
    """Add and Edit Extra Expenses Details"""
    extra_expenses_id = models.AutoField(primary_key=True)
    extra_expenses = models.CharField(max_length=70, blank=False, null=False)

    def __str__(self):
        return self.extra_expenses

class Places(models.Model):
    """A centrailised database of places added in enquiry form etc"""

    # Defining Source/Destination choices. This is to store if the place
    # stored belongs to source or detination or return location of enquiry.
    Source = 'Source'
    Destination = 'Destination'
    Return = 'Return'
    src_dest_choices = (
        (Source, 'Source'),
        (Destination, 'Destination'),
        (Return, 'Return'),
    )

    place_id = models.AutoField(primary_key=True)
    enquiry_id = models.ForeignKey('quotes.Enquiry', related_name='places', 
                                    on_delete=models.PROTECT)
    place = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=18, decimal_places=14, blank=True, null=True)
    lng = models.DecimalField(max_digits=18, decimal_places=14, blank=True, null=True)
    src_dest = models.CharField(max_length=20, choices=src_dest_choices,
                                blank=False)

    def __str__(self):
        return self.place
