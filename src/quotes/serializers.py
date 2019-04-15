"""
Serializers for the Quotes Module
"""
from rest_framework import serializers
from masters.serializers import (VehicleBodySerializer, VehicleTypeSerializer,
    ExtraExpensesSerializer, PlacesSerializer)
from quotes.models import Enquiry, SupplierQuote
# Defining serializers for quotes app

class EnquirySerializer(serializers.ModelSerializer):
    """
    Enquiry Model Serializer.
    """

    # vehicle_body_str = serializers.StringRelatedField(source='vehicle_body', many=True)
    vehicle_body_obj = VehicleBodySerializer(source='vehicle_body', many=True, read_only=True)
    vehicle_type_obj = VehicleTypeSerializer(source='vehicle_type', many=True, read_only=True)
    extra_expenses_obj = ExtraExpensesSerializer(source='extra_expenses', many=True, read_only=True)
    vehicle_body_str = serializers.StringRelatedField(source='vehicle_body', many=True)
    vehicle_type_str = serializers.StringRelatedField(source='vehicle_type', many=True)
    extra_expenses_str = serializers.StringRelatedField(source='extra_expenses', many=True)
    places_obj = PlacesSerializer(source='places', many=True, read_only=False)
    places_str = serializers.StringRelatedField(source='places', many=True)

    class Meta:
        model = Enquiry
        fields = ('enquiry_id', 'status', 'length', 'width', 'height', 'weight',
                    'vehicle_type', 'vehicle_body', 'extra_expenses', 'load_type',
                    'comments', 'enquiry_no', 'loading_date', 'created', 'places', 'places_str', 
                    'places_obj', 'vehicle_type_str', 'vehicle_type_obj', 'vehicle_body_str', 
                    'vehicle_body_obj', 'extra_expenses_str', 'extra_expenses_obj')

class SupplierQuoteSerializer(serializers.ModelSerializer):
    """
    SupplierQuotes Model Serializer.
    """
    class Meta:
        model = SupplierQuote
        fields = '__all__'
