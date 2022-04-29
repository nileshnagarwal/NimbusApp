"""
Models for the Operations Module. This module has all the models
required for operations like challan, lr, invoice etc.
"""

from django.db import models
from datetime import date
from django.contrib.auth import get_user_model

def get_sentinel_user():
    return get_user_model().objects.get_or_create(email='deleted@nimbuslogistics.in')[0]

class LorryReceiptNo(models.Model):
    """
    LR_No model to engage LR no which will be used in LR model as
    foreignkey
    """

    lr_no = models.IntegerField(primary_key=True)
    verification_no = models.CharField(max_length=6, blank=True, null=False)
    client_id = models.ForeignKey('masters.Client', null=False, 
                                blank=False, on_delete=models.PROTECT)
    vehicle_no = models.CharField(max_length=12, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(get_user_model(), blank=True,null=True, 
                            on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return "LR No: %s" %(str(self.lr_no))

class LorryReceipt(models.Model):
    """
    LR Model
    """

    lr_no_id = models.OneToOneField('LorryReceiptNo', on_delete=models.PROTECT, null=False,
            blank=False, primary_key=True, related_name='lr_details')
    date = models.DateTimeField(null=False, blank=False)
    vehicle_no = models.CharField(max_length=12, blank=False, null=False)
    dispatch_from = models.CharField(max_length=255, blank=False, null=False)
    ship_to = models.CharField(max_length=255, blank=False, null=False)
    consignor_id = models.ForeignKey('masters.ClientAddress', 
            on_delete=models.PROTECT, null=True, blank=True, related_name='lr_consignor')
    consignee_id = models.ForeignKey('masters.ClientAddress', on_delete=models.PROTECT,
                null=True, blank=True, related_name='lr_consignee')
    consignor_manual = models.TextField(max_length=500, blank=True, null=True)
    consignee_manual = models.TextField(max_length=500, blank=True, null=True)
    consignor_gstin = models.CharField(max_length=255, blank=True, null=True)
    consignee_gstin = models.CharField(max_length=255, blank=True, null=True)
    invoice_no = models.CharField(max_length=255, blank=True, null=True)
    invoice_date = models.CharField(max_length=255, blank=True, null=True)
    dc_no = models.CharField(max_length=255, blank=True, null=True)
    dc_date = models.CharField(max_length=255, blank=True, null=True)
    boe_no = models.CharField(max_length=255, blank=True, null=True)
    boe_date = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255, blank=False, null=False)
    ewaybill_no = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    challan_no = models.IntegerField(blank=False, null=False)
    ewaybill_expiry_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(get_user_model(), blank=True,null=True, 
                            on_delete=models.SET(get_sentinel_user))


    def __str__(self):
        return "Detailed %s" %(str(self.lr_no_id))

class Item(models.Model):
    """
    Item Model for entering multiple items in LR
    """

    item_id = models.AutoField(primary_key=True)
    packing_type = models.CharField(max_length=255, null=True, blank=True)
    no_of_pkg = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=False, blank=False)
    lr_no_id = models.ForeignKey('LorryReceipt', on_delete=models.PROTECT, 
            blank=False, null=False, related_name='item')

    def __str__(self):
        return "Item for %s" %(str(self.lr_no_id.lr_no_id))