from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import VehicleType, VehicleBody, Transporter, ExtraExpenses

# Register your models here.
admin.site.register(VehicleType)
admin.site.register(VehicleBody)
admin.site.register(ExtraExpenses)

class TransporterResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = Transporter
        # import_id_fields defines the field to be used as id
        import_id_fields = ('transporter_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('transporter_id', 'transporter', 'primary_mobile',  'primary_person',
                    'other_contact', 'address', 'office_location', 'office_lat', 'office_lng', )

class TransporterAdmin(ImportExportModelAdmin):
    resource_class = TransporterResource

admin.site.register(Transporter, TransporterAdmin)