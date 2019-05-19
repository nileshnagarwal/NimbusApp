"""
Serializers for the Quotes Module
"""
from rest_framework import serializers
from masters.serializers import (VehicleBodySerializer, VehicleTypeSerializer,
    ExtraExpensesSerializer, PlacesSerializer)
from quotes.models import Enquiry, SupplierQuote
from masters.models import Places

# Defining serializers for quotes app

class EnquirySerializer(serializers.ModelSerializer):
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

    def get_source(self, enquiry):
        qs = Places.objects.filter(src_dest="Source", enquiry_id=enquiry.enquiry_id)
        serializer = PlacesSerializer(instance=qs, many=True)
        places = serializer.data
        places_arr = [d['place'] for d in places if 'place' in d]
        return places_arr
    
    def get_destination(self, enquiry):
        qs = Places.objects.filter(src_dest="Destination", enquiry_id=enquiry.enquiry_id)
        serializer = PlacesSerializer(instance=qs, many=True)
        places = serializer.data
        places_arr = [d['place'] for d in places if 'place' in d]
        return places_arr

    def get_return(self, enquiry):
        qs = Places.objects.filter(src_dest="Return", enquiry_id=enquiry.enquiry_id)
        serializer = PlacesSerializer(instance=qs, many=True)
        places = serializer.data
        places_arr = [d['place'] for d in places if 'place' in d]
        return places_arr

    def get_source_obj(self, enquiry):
        qs = Places.objects.filter(src_dest="Source", enquiry_id=enquiry.enquiry_id)
        serializer = PlacesSerializer(instance=qs, many=True)
        places = serializer.data
        return places 
    
    def get_destination_obj(self, enquiry):
        qs = Places.objects.filter(src_dest="Destination", enquiry_id=enquiry.enquiry_id)
        serializer = PlacesSerializer(instance=qs, many=True)
        places = serializer.data
        return places 
        
    class Meta:
        model = Enquiry
        # We define the fields manually to add 'places' to the list of fields as it does not
        # get added automatically being a reverse foreign key field.
        fields = ('enquiry_id', 'status', 'length', 'width', 'height', 'weight',
                    'vehicle_type', 'vehicle_body', 'extra_expenses', 'load_type',
                    'comments', 'enquiry_no', 'loading_date', 'created', 'places_str', 
                    'places_obj', 'vehicle_type_str', 'vehicle_type_obj', 'vehicle_body_str', 
                    'vehicle_body_obj', 'extra_expenses_str', 'extra_expenses_obj', 'user', 'places_source',
                    'places_destination', 'places_return', 'places_source_obj', 'places_destination_obj')

class SupplierQuoteSerializer(serializers.ModelSerializer):
    """
    SupplierQuotes Model Serializer.
    """
    class Meta:
        model = SupplierQuote
        fields = '__all__'