from django import forms
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.db import models

from .models import LorryReceipt, LorryReceiptNo, Item

# Register your models here.

class LorryReceiptNoResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = LorryReceiptNo
        # import_id_fields defines the field to be used as id
        import_id_fields = ('lr_no',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('lr_no', 'verification_no','client_id', 'vehicle_no', 'created', 
            'modified', 'user_id', )

class LorryReceiptNoAdmin(ImportExportModelAdmin):
    resource_class = LorryReceiptNoResource

admin.site.register(LorryReceiptNo, LorryReceiptNoAdmin)

class LorryReceiptResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = LorryReceipt
        # import_id_fields defines the field to be used as id
        import_id_fields = ('lr_no_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('lr_no_id', 'date', 'vehicle_no', 'dispatch_from', 'ship_to', 'consignor_id',
                    'consignee_id', 'consignor_manual', 'consignee_manual', 'consignor_gstin', 
                    'consignee_gstin', 'invoice_no', 'invoice_date', 'dc_no', 'dc_date',
                    'boe_no', 'boe_date', 'value', 'ewaybill_no', 'comment', 'size', 'weight', 
                    'challan_no', 'ewaybill_expiry_date', 'created', 'modified', 'user_id', )

class LorryReceiptAdmin(ImportExportModelAdmin):
    resource_class = LorryReceiptResource

admin.site.register(LorryReceipt, LorryReceiptAdmin)

class ItemResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = Item
        # import_id_fields defines the field to be used as id
        import_id_fields = ('item_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('item_id', 'packing_type', 'no_of_pkg', 'description', 'lr_no_id', )

class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource

admin.site.register(Item, ItemAdmin)
