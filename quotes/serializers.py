"""
Serializers for the Quotes Module
"""
from rest_framework import serializers
from masters.serializers import (VehicleBodySerializer, VehicleTypeSerializer,
    ExtraExpensesSerializer, PlacesSerializer, TransporterProfileSerializer)
from quotes.models import Enquiry, SupplierQuote, SupplierResponse
from masters.models import Places, TransporterProfile, LoadType
from common.serializers import UserSerializer

# Defining serializers for quotes app

class EnquirySerializer(serializers.ModelSerializer):
    """
    Enquiry Model Basic ModelSerializer. 
    Has only the fields present in the model.
    """
    class Meta:
        model = Enquiry
        fields = '__all__'

class EnquirySerializer(serializers.ModelSerializer):
    """
    Enquiry Model Basic ModelSerializer. 
    Has only the fields present in the model.
    """
    class Meta:
        model = Enquiry
        fields = '__all__'

class EnquiryDetailedSerializer(serializers.ModelSerializer):
    """
    Enquiry Model Serializer.
    """

    # We need to return relational fields with all the data filled to the front end.
    # Hence we define some new fields below. obj fields are adding the whole object
    # of the related field and str fields are addding only the __str__ repr of the 
    # related field.
    vehicle_body_obj = VehicleBodySerializer(source='vehicle_body', many=True, read_only=True)
    vehicle_type_obj = VehicleTypeSerializer(source='vehicle_type', many=True, read_only=True)
    extra_expenses_obj = ExtraExpensesSerializer(source='extra_expenses', many=True, read_only=True)
    vehicle_body_str = serializers.StringRelatedField(source='vehicle_body', many=True, read_only=True)
    vehicle_type_str = serializers.StringRelatedField(source='vehicle_type', many=True, read_only=True)
    extra_expenses_str = serializers.StringRelatedField(source='extra_expenses', many=True, read_only=True)
    places_obj = PlacesSerializer(source='places', many=True, read_only=True)
    places_str = serializers.StringRelatedField(source='places', many=True, read_only=True)
    places_source = serializers.SerializerMethodField('get_source', read_only=True)
    places_destination = serializers.SerializerMethodField('get_destination', read_only=True)
    places_return = serializers.SerializerMethodField('get_return', read_only=True)
    places_source_obj = serializers.SerializerMethodField('get_source_obj', read_only=True)
    places_destination_obj = serializers.SerializerMethodField('get_destination_obj', read_only=True)
    load_size = serializers.SerializerMethodField('get_load_size', read_only=True)
    load_type_str = serializers.StringRelatedField(source='load_type_new', read_only=True)

    def get_source(self, enquiry):
        return get_source(self, enquiry.enquiry_id)
    
    def get_destination(self, enquiry):
        return get_destination(self, enquiry.enquiry_id)

    def get_return(self, enquiry):
        qs = Places.objects.filter(src_dest="Return", enquiry_id=enquiry.enquiry_id).order_by('place_id')
        serializer = PlacesSerializer(instance=qs, many=True)
        places = serializer.data
        places_arr = [d['place'] for d in places if 'place' in d]
        return places_arr

    def get_source_obj(self, enquiry):
        qs = Places.objects.filter(src_dest="Source", enquiry_id=enquiry.enquiry_id).order_by('place_id')
        serializer = PlacesSerializer(instance=qs, many=True)
        places = serializer.data
        return places 
    
    def get_destination_obj(self, enquiry):
        qs = Places.objects.filter(src_dest="Destination", enquiry_id=enquiry.enquiry_id).order_by('place_id')
        serializer = PlacesSerializer(instance=qs, many=True)
        places = serializer.data
        return places 

    def get_load_size(self, enquiry):
        return (f'{enquiry.length:.2f} x {enquiry.width:.2f} x {enquiry.height:.2f}')
        
    class Meta:
        model = Enquiry
        # We define the fields manually to add 'places' to the list of fields as it does not
        # get added automatically being a reverse foreign key field.
        fields = ('enquiry_id', 'status', 'length', 'width', 'height', 'weight',
                    'vehicle_type', 'vehicle_body', 'extra_expenses', 'load_type_new', 'load_type_str',
                     'load_size', 'comments', 'enquiry_no', 'loading_date', 'created', 'places_str', 
                    'places_obj', 'vehicle_type_str', 'vehicle_type_obj', 'vehicle_body_str', 
                    'vehicle_body_obj', 'extra_expenses_str', 'extra_expenses_obj', 'user', 'places_source',
                    'places_destination', 'places_return', 'places_source_obj', 'places_destination_obj',
                    'cnf_enquiry_no', 'cnf_loading_date', 'cnf_comments', 'cnf_created', 'modified')


class SupplierQuoteSerializer(serializers.ModelSerializer):
    """
    SupplierQuotes Model Serializer.
    """
    transporter_str = serializers.StringRelatedField(source='transporter_id', read_only=True)
    enquiry_no = serializers.StringRelatedField(source='enquiry_id', read_only=True)
    places_source = serializers.SerializerMethodField('get_source', read_only=True)
    places_destination = serializers.SerializerMethodField('get_destination', read_only=True)
    enquiry = EnquirySerializer(source='enquiry_id', read_only=True)
    linked_trans_profile = serializers.SerializerMethodField('get_linked_trans_profiles', read_only=True)
    traffic_incharge = UserSerializer(source='user_id', read_only=True)
    
    def get_source(self, quote):
        return get_source(self, quote.enquiry_id)

    def get_destination(self, quote):
        return get_destination(self, quote.enquiry_id)

    def get_linked_trans_profiles(self, quote):
        qs = TransporterProfile.objects.filter(quote_id=quote)
        serializer = TransporterProfileSerializer(qs, many=True)
        return serializer.data

    def validate(self, data):
        """
        Check if either the freight_incl or freight_excl or freight_normal is provided
        """
        # Get enquiry instance
        enquiry = Enquiry.objects.get(pk=data['enquiry_id'].enquiry_id)
        self.validate_update_freight(data)
        # If load_type is ODC, either incl or excl freight must be provided
        if (enquiry.load_type_new.load_type==LoadType.ODC):
            if (data['freight_incl_org'] is None and data['freight_excl_org'] is None):
                raise serializers.ValidationError("For " + LoadType.ODC + " cargo, " + \
                    "either freight_incl_org or freight_excl_org should be provided.")
        # Else normal freight must be provided
        else:
            if (data['freight_normal_org'] is None):
                raise serializers.ValidationError("Freight needs to be provided.")
        return super().validate(data)
    
    def validate_update_freight(self, data):
        if (self.instance):
            print("Update")
            print(data)
            load_type_str = self.instance.enquiry_id.load_type_new.load_type
            if (load_type_str==LoadType.Normal or load_type_str==LoadType.Container or \
                load_type_str==LoadType.Part):
                if (data['freight_normal']):
                    data['freight_excl'] = None
                    data['freight_incl'] = None
                    if (self.instance.freight_normal_rev is None):
                        if (data['freight_normal']<self.instance.freight_normal_org):
                            return data
                        else: raise serializers.ValidationError("Revised Freight should be less" +\
                            " than the original Freight.")
                    elif (data['freight_normal']<self.instance.freight_normal_rev):
                        return data
                    else: raise serializers.ValidationError("Revised Freight should be less" +\
                            " than the original Freight.")
                else:
                    raise serializers.ValidationError("For Normal Size Cargo, freight_normal should be" +\
                        " provided")
            elif (load_type_str==LoadType.ODC):
                if (data["freight_excl"] or data["freight_incl"]):
                    data['freight_normal'] = None
                    if (data['freight_excl']):
                        if(self.instance.freight_incl_rev is None):
                            if (data['freight_excl']<self.instance.freight_excl_org):
                                return data
                            else: raise serializers.ValidationError("Revised Freight should be less" +\
                                " than the original Freight.")
                        elif (data['freight_excl']<self.instance.freight_excl_rev):
                            return data
                        else: raise serializers.ValidationError("Revised Freight should be less" +\
                                " than the original Freight.")
                    if (data['freight_incl']):
                        if(self.instance.freight_incl_rev is None):
                            if (data['freight_incl']<self.instance.freight_incl_org):
                                return data
                            else: raise serializers.ValidationError("Revised Freight should be less" +\
                                " than the original Freight.")
                        elif (data['freight_incl']<self.instance.freight_incl_rev):
                            return data
                        else: raise serializers.ValidationError("Revised Freight should be less" +\
                                " than the original Freight.")
                else: 
                    raise serializers.ValidationError("For ODC Size Cargo, freight_excl or freight_incl" +\
                        "  should be provided")
        else:
            print("Creation")

    class Meta:
        model = SupplierQuote
        fields = '__all__'

def get_source(self, enquiry_id):
    qs = Places.objects.filter(src_dest="Source", enquiry_id=enquiry_id).order_by('place_id')
    serializer = PlacesSerializer(instance=qs, many=True)
    places = serializer.data
    places_arr = [d['place'] for d in places if 'place' in d]
    return places_arr

def get_destination(self, enquiry_id):
    qs = Places.objects.filter(src_dest="Destination", enquiry_id=enquiry_id).order_by('place_id')
    serializer = PlacesSerializer(instance=qs, many=True)
    places = serializer.data
    places_arr = [d['place'] for d in places if 'place' in d]
    return places_arr

class SupplierResponseSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Supplier Responses
    """
    class Meta:
        model = SupplierResponse
        fields = '__all__'
