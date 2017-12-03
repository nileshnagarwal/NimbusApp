from rest_framework import serializers
from quotes.models import Enquiry, SupplierQuote
# Defining serializers for quotes app

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'

class SupplierQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierQuote
        fields = '__all__'

                  