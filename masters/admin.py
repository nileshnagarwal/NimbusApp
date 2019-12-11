from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import VehicleType, VehicleBody, LoadType, \
    Transporter, ExtraExpenses, District, TransporterProfile,\
    Places

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
                    'state', 'unique_id', 'neighbors', 'neighbors_str', )

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
        fields = ('trans_profile_id', 'transporter_id', 'source_id', 'destination_id',
                    'vehicle_type_id', 'load_type', )

class TransProfileAdmin(ImportExportModelAdmin):
    resource_class = TransProfileResource

class PlacesResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = Places
        # import_id_fields defines the field to be used as id
        import_id_fields = ('place_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('place_id', 'enquiry_id', 'place', 'lat',
                    'lng', 'place_id_agm', 'src_dest', 'district_id', 
                    'address', 'sublocality_level_1', 'locality', 
                    'administrative_area_level_2', 'administrative_area_level_1', )

class PlacesAdmin(ImportExportModelAdmin):
    resource_class = PlacesResource

class VehicleTypeResource(resources.ModelResource):
    """
    Refer: https://django-import-export.readthedocs.io/en/latest/
    getting_started.html#creating-import-export-resource
    """

    class Meta:
        model = VehicleType
        # import_id_fields defines the field to be used as id
        import_id_fields = ('vehicle_type_id',)
        # When import_id_fields is used, fields need to be explicitly specified
        fields = ('vehicle_type_id', 'vehicle', 'length', 'width',
                    'height', 'weight', 'category', )

class VehicleTypeAdmin(ImportExportModelAdmin):
    resource_class = VehicleTypeResource

# Register your models here.
admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(VehicleBody)
admin.site.register(LoadType)
admin.site.register(ExtraExpenses)
admin.site.register(Transporter, TransporterAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(TransporterProfile, TransProfileAdmin)
admin.site.register(Places, PlacesAdmin)
