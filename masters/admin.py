from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import VehicleType, VehicleBody, LoadType, \
    Transporter, ExtraExpenses, District, TransporterProfile

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

class DistrictResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = District
        # import_id_fields defines the field to be used as id
        import_id_fields = ('district_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('district_id', 'district', 'lat',  'lng',
                    'state', )

class DistrictAdmin(ImportExportModelAdmin):
    resource_class = DistrictResource

class TransProfileResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = TransporterProfile
        # import_id_fields defines the field to be used as id
        import_id_fields = ('trans_profile_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('transproter_id', 'source_id', 'destination_id',  'vehicle_type_id',
                    'load_type', )

class TransProfileAdmin(ImportExportModelAdmin):
    resource_class = TransProfileResource

# Register your models here.
admin.site.register(VehicleType)
admin.site.register(VehicleBody)
admin.site.register(LoadType)
admin.site.register(ExtraExpenses)
admin.site.register(Transporter, TransporterAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(TransporterProfile, TransProfileAdmin)