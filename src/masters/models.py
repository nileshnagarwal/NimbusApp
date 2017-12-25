from django.db import models
from webapp import fields

# Create your models here.
class Vehicle_type(models.Model):
    """Defining vehicle types like 40' High Bed 20T, 40' Low Bed 20T
    etc.""" 
    vehicle_type_id = models.AutoField(primary_key=True)
    vehicle = models.CharField(max_length=20, blank=False, null=False)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.vehicle

class Vehicle_body(models.Model):
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
    primary_contact = models.CharField(max_length=255, blank=True, null=True)
    primary_person = models.CharField(max_length=40, blank=True, null=True)
    other_contact = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.transporter
