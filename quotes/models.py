"""
Models for the Quotes Module
"""

from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from masters.models import Transporter

def get_sentinel_user():
    return get_user_model().objects.get_or_create(email='deleted@nimbuslogistics.in')[0]

# Creating enquiry model.
class Enquiry(models.Model):
    """
    Create enquiries that are in Quote Retrieval stage or have
    been finalised
    """
    # Defining choices for status and load type fields.
    # Status choice fields
    FloatedEnquiry = 'Floated Enquiry'
    UnfloatedEnquiry = 'Unfloated Enquiry'
    FinalisedOrder = 'Confirmed Order'
    _status_choices = (
        (FloatedEnquiry, 'Floated Enquiry'),
        (UnfloatedEnquiry, 'Unfloated Enquiry'),
        (FinalisedOrder, 'Confirmed Order'),
    )
    
    # Defining model fields
    enquiry_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=_status_choices,
                              default=UnfloatedEnquiry, blank=False)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    # Since vehicle_type and vehicle_body may be required to alter from admin
    # panel for multiple times in the future, we are defining them as seperate
    # models and using ForeignKey to connect the models in many to one
    # relationship.
    vehicle_type = models.ManyToManyField('masters.VehicleType', blank=True)
    vehicle_body = models.ManyToManyField('masters.VehicleBody', blank=True)
    extra_expenses = models.ManyToManyField('masters.ExtraExpenses',
                                            blank=True)    
    load_type_new = models.ForeignKey('masters.LoadType', blank=True, 
                                null=True, on_delete=models.PROTECT)
    comments = models.TextField(blank=True, null=True)
    enquiry_no = models.CharField(max_length=255, blank=True, null=True)
    loading_date = models.DateTimeField(default=date.today)
    created = models.DateTimeField(auto_now_add=True)
    # get_user_model() is used to get the current AUTH_USER_MODEL defined in settings. 
    # Refer: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
    user = models.ForeignKey(get_user_model(), blank=False,null=False, 
                            on_delete=models.SET(get_sentinel_user))
    modified = models.DateTimeField(auto_now=True)
    cnf_enquiry_no = models.CharField(max_length=255, blank=True, null=True)        
    cnf_loading_date = models.DateTimeField(blank=True, null=True)
    cnf_comments = models.TextField(blank=True, null=True)
    cnf_created = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.enquiry_no


class SupplierQuote(models.Model):
    """
    Enter the quotes received from vendors for the received enquiries.
    """
    quote_id = models.AutoField(primary_key=True)
    enquiry_id = models.ForeignKey('Enquiry', blank=False, null=True,
                                on_delete=models.PROTECT)
    transporter_id = models.ForeignKey('masters.Transporter', blank=False,
                                    null=True, on_delete=models.PROTECT)
    freight = models.PositiveIntegerField(blank=True, null=True)
    freight_incl_rev = models.PositiveIntegerField(blank=True, null=True)
    freight_excl_rev = models.PositiveIntegerField(blank=True, null=True)
    freight_normal_rev = models.PositiveIntegerField(blank=True, null=True)
    freight_incl_org = models.PositiveIntegerField(blank=True, null=True)
    freight_excl_org = models.PositiveIntegerField(blank=True, null=True)
    freight_normal_org = models.PositiveIntegerField(blank=True, null=True)
    including_fine = models.CharField(max_length=20, null=True, blank=True)
    vehicle_avail = models.CharField(max_length=20, null=True, blank=True)
    vehicle_type_id = models.ManyToManyField('masters.VehicleType')
    vehicle_body_id = models.ManyToManyField('masters.VehicleBody', blank=True)
    # get_user_model() is used to get the current AUTH_USER_MODEL defined in settings. 
    # Refer: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
    user_id = models.ForeignKey(get_user_model(), blank=False,null=False, on_delete=models.SET(get_sentinel_user))
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Enq#%s - %s' %(self.enquiry_id, self.transporter_id)

class SupplierResponse(models.Model):
    """
    Record responses received from calls to suppliers.
    """

    searching_vehicle = "searching vehicle"
    vehicle_unloading = "vehicle unloading"
    not_avail = "not available"
    avail = "available"
    na = "status unknown"
    awaiting_rates = 'awaiting rates'
    not_interested = 'not interested'
    incorrect_match = 'incorrect match'

    vehicle_status_options = [
        searching_vehicle,
        vehicle_unloading,
        not_avail,
        avail,
        na,
    ]

    call_status_options = [
        awaiting_rates,
        incorrect_match,
        not_interested,
    ]

    _response_choices = (
        (searching_vehicle, 'Searching Vehicle'),
        (vehicle_unloading, 'Vehicle Unloading'),
        (not_avail, 'Not Available'),
        (avail, 'Available'),
        (na, 'Status Unknown'),
        (awaiting_rates, 'Awaiting Rates'),
        (not_interested, 'Not Interested'),
        (incorrect_match, 'Incorrect Match'),
    )

    response_id = models.AutoField(primary_key=True)
    enquiry_id = models.ForeignKey('Enquiry', blank=False, null=False, on_delete=models.PROTECT)
    transporter_id = models.ForeignKey('masters.Transporter', blank=False, null=False, on_delete=models.PROTECT)
    quote_id = models.ForeignKey('SupplierQuote', blank=True, null=True, related_name='response', on_delete=models.SET_NULL)
    response = models.CharField(max_length=20, choices=_response_choices, blank=False, null=False)

    def __str__(self):
        return '%s: %s - %s' %(self.transporter_id, self.enquiry_id, self.response)