"""
Models for the Masters Module. This Module has all the masters data which is
used as foreignkeys in other forms.
"""

from django.db import models
from django.contrib.postgres.fields import JSONField

from webapp.validators import MobileValidation

# Create your models here.
class VehicleType(models.Model):
    """
    Defining vehicle types like 40' High Bed 20T, 40' Low Bed 20T
    etc.
    """

    # Defining choices for category field
    # Category choice fields
    Trailer = 'Trailer'
    Truck = 'Truck'
    Tempo = 'Tempo'
    OpenTruck = 'Open Truck'
    ContainerTruck = 'Container Truck'
    HydraulicTrailer = 'Hydraulic Trailer'
    Misc = 'Misc'
    
    _cat_choices = (
        (Trailer, 'Trailer'),
        (Truck, 'Truck'),
        (Tempo, 'Tempo'),
        (OpenTruck, 'Open Truck'),
        (ContainerTruck, 'Container Truck'),
        (HydraulicTrailer, 'Hydraulic Trailer'),
        (Misc, 'Misc'),
    )

    vehicle_type_id = models.AutoField(primary_key=True)
    vehicle = models.CharField(max_length=30, blank=False, null=False)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=30, choices=_cat_choices,
                                default=Misc, blank=False, null=False)

    def __str__(self):
        return self.vehicle

class VehicleBody(models.Model):
    """Defining vehicle body type like half body, full body, open body
     etc."""
    vehicle_body_id = models.AutoField(primary_key=True)
    body = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.body

class LoadType(models.Model):
    """
    Defining load type like ODC, Normal etc.
    """
    # Load type choice fields. Used in logical expressions.
    ODC = 'ODC'
    Normal = 'Normal'
    Part = 'Part'
    Container = 'Container'
    OdcContainer = 'ODC Container'
    _load_type_choices = (
        (ODC, 'ODC'),
        (Normal, 'Normal'),
        (Part, 'Part'),
        (OdcContainer, 'ODC Container'),
    )

    odc = 'ODC'
    ftl = 'FTL'
    ltl = 'LTL'
    _load_size_choices = (
        (odc, 'ODC'),
        (ftl, 'FTL'),
        (ltl, 'LTL'),
    )

    load_type_id = models.AutoField(primary_key=True)
    load_type = models.CharField(max_length=20, blank=False, null=False)
    load_size = models.CharField(max_length=20, choices=_load_size_choices,
                                    blank=True, null=True)

    def __str__(self):
        return self.load_type

class Transporter(models.Model):
    """Add and Edit Transporter Details"""
    transporter_id = models.AutoField(primary_key=True)
    transporter = models.CharField(max_length=70, blank=False, null=False)
    primary_mobile = models.CharField(max_length=10,
        validators=[MobileValidation(length=10, start_with='6-9')], blank=False, null=False)
    primary_person = models.CharField(max_length=40, blank=True, null=True)
    other_contact = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    office_location = models.CharField(max_length=255, blank=True, null=True)
    office_lat = models.DecimalField(max_digits=24, decimal_places=20, blank=True, null=True)
    office_lng = models.DecimalField(max_digits=24, decimal_places=20, blank=True, null=True)


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
    # Related Name is used to define reverse relation in enquiry serializer
    # Refer: https://www.django-rest-framework.org/api-guide/relations/#reverse-relations
    enquiry_id = models.ForeignKey('quotes.Enquiry', related_name='places', 
                                    on_delete=models.PROTECT)
    place = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=24, decimal_places=20, blank=True, null=True)
    lng = models.DecimalField(max_digits=24, decimal_places=20, blank=True, null=True)
    place_id_agm = models.CharField(max_length=255)
    src_dest = models.CharField(max_length=20, choices=src_dest_choices,
                                blank=False)
    district_id = models.ForeignKey('District', related_name='place',
                                    on_delete=models.PROTECT, blank=True, null=True)
    address = JSONField(blank=True, null=True)
    sublocality_level_1 = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    administrative_area_level_2 = models.CharField(max_length=255, blank=True, null=True)
    administrative_area_level_1 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.place

class District(models.Model):
    """
    Model for storing District Names with respective data like lat, lng etc
    """
    district_id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=255, blank=False, null=False)
    state = models.CharField(max_length=255, blank=False, null=False)
    lat = models.DecimalField(max_digits=24, decimal_places=20, blank=True, null=True)
    lng = models.DecimalField(max_digits=24, decimal_places=20, blank=True, null=True)
    unique_id = models.CharField(max_length=20, blank=True, null=True)
    neighbors = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return '%s, %s' %(self.district, self.state)

class TransporterProfile(models.Model):
    """
    Model for storing Transporter Business Profile which helps search the right 
    transporter for each enquiry
    """

    trans_profile_id = models.AutoField(primary_key=True)
    transporter_id = models.ForeignKey('masters.Transporter', related_name='trans_profile',
                        on_delete=models.PROTECT, blank=False, null=False)
    source_id = models.ManyToManyField('masters.District', related_name='trans_profile_source',
                        blank=False)
    destination_id = models.ManyToManyField('masters.District',
                        related_name='trans_profile_dest', blank=False)
    vehicle_type_id = models.ManyToManyField('masters.VehicleType',
                        related_name='trans_profile_veh_type', blank=False)
    load_type = models.ManyToManyField('masters.LoadType', related_name='trans_profile_load_type',
                        blank=False)
    quote_id = models.ForeignKey('quotes.SupplierQuote', related_name='linked_trans_profiles', 
                        on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return 'Transporter Profile: %s, Transporter: %s' %(self.trans_profile_id, self.transporter_id)

class Client(models.Model):
    """
    Client Details Model
    """

    client_id = models.AutoField(primary_key=True)
    client = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.client

class ClientAddress(models.Model):
    """
    A model to store various client addresses with respective GSTIN
    """

    client_address_id = models.AutoField(primary_key=True)
    address = models.TextField(max_length=500, null=False, blank=False)
    gstin = models.CharField(max_length=15, null=True, blank=True)
    client_id = models.ForeignKey('Client', on_delete=models.PROTECT,
            blank=False, null=False)
    
    def __str__(self):
        return "Details of %s" %(self.client_id)