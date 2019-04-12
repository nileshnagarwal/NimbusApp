"""
Models for the Quotes Module
"""

from datetime import date
from django.db import models
from django.contrib.auth import get_user_model


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
    status_choices = (
        (FloatedEnquiry, 'Floated Enquiry'),
        (UnfloatedEnquiry, 'Unfloated Enquiry'),
        (FinalisedOrder, 'Confirmed Order'),
    )
    # Load type choice fields
    ODC = 'ODC'
    Normal = 'Normal'
    Part = 'Part'
    Container = 'Container'
    load_type_choices = (
        (ODC, 'ODC'),
        (Normal, 'Normal'),
        (Part, 'Part'),
        (Container, 'Container'),
    )

    # Defining model fields
    enquiry_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=status_choices,
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
    load_type = models.CharField(max_length=10, choices=load_type_choices,
                                 default=Normal, blank=False)
    comments = models.TextField(blank=True, null=True)
    enquiry_no = models.CharField(max_length=255, blank=True, null=True)
    loading_date = models.DateTimeField(default=date.today)
    created = models.DateTimeField(auto_now_add=True)
    # get_user_model() is used to get the current AUTH_USER_MODEL defined in settings. 
    # Refer: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
    user = models.ForeignKey(get_user_model(), blank=False,null=False)

    def __str__(self):
        return 'Deal No:%s' %(self.enquiry_no)

class SupplierQuote(models.Model):
    """
    Enter the quotes received from vendors for the received enquiries.
    """
    quote_id = models.AutoField(primary_key=True)
    enquiry = models.ForeignKey('Enquiry', blank=False, null=True,
                                on_delete=models.SET_NULL)
    transporter = models.ForeignKey('masters.Transporter', blank=False,
                                    null=True, on_delete=models.SET_NULL)
    rate = models.PositiveIntegerField(blank=False, null=False)
    including_fine = models.BooleanField()
    vehicle_avail = models.BooleanField()
    vehicle_type = models.ManyToManyField('masters.VehicleType')
    # get_user_model() is used to get the current AUTH_USER_MODEL defined in settings. 
    # Refer: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
    user = models.ForeignKey(get_user_model(), blank=False,null=False,default=4)
