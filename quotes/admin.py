from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Enquiry, SupplierQuote

class EnquiryResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = Enquiry
        # import_id_fields defines the field to be used as id
        import_id_fields = ('enquiry_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('enquiry_id', 'status', 'length', 'width', 'height', 'weight',
                    'vehicle_type', 'vehicle_body', 'extra_expenses', 'load_type', 
                    'comments', 'enquiry_no', 'loading_date', 'created', 'user', )

class EnquiryAdmin(ImportExportModelAdmin):
    resource_class = EnquiryResource

admin.site.register(Enquiry, EnquiryAdmin)

class SupplierQuoteResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = SupplierQuote
        # import_id_fields defines the field to be used as id
        import_id_fields = ('quote_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('quote_id', 'enquiry_id', 'transporter_id', 'freight', 'including_fine',
                    'vehicle_avail', 'vehicle_type_id', 'vehicle_body_id', 'user_id',
                    'comments', 'created', 'transporter_id__transporter', )

class SupplierQuoteAdmin(ImportExportModelAdmin):
    resource_class = SupplierQuoteResource

admin.site.register(SupplierQuote, SupplierQuoteAdmin)