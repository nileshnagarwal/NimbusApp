"""
Serializers for the Quotes Module
"""
from rest_framework import serializers
from quotes.models import Enquiry, SupplierQuote
# Defining serializers for quotes app

class EnquirySerializer(serializers.ModelSerializer):
    """
    Enquiry Model Serializer.
    """
    class Meta:
        model = Enquiry
        fields = '__all__'

class SupplierQuoteSerializer(serializers.ModelSerializer):
    """
    SupplierQuotes Model Serializer.
    """
    class Meta:
        model = SupplierQuote
        fields = '__all__'
