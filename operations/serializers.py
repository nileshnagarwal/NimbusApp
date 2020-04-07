"""
Serializers for Operations Module
"""

from rest_framework import serializers
from .models import LorryReceipt, LorryReceiptNo, Item
from masters.serializers import ClientSerializer

class LorryReceiptNoSerializer(serializers.ModelSerializer):
    """
    Model Serializer for LorryReceiptNo Model
    """
    client = ClientSerializer(source='client_id', read_only=True)

    class Meta:
        model = LorryReceiptNo
        fields = '__all__'

class LorryReceiptSerializer(serializers.ModelSerializer):
    """
    Model Serializer for LorryReceipt Model
    """
    class Meta:
        model = LorryReceipt
        fields = '__all__'

    # to_internal_value converts the value to avoid validation error
    # Without this we get error saying weight should be an integer
    # despite having null=True and default=0
    def to_internal_value(self, data):
        if data.get('weight') == '':
            data['weight'] = 0
        
        return super(LorryReceiptSerializer, self).to_internal_value(data)

class ItemSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Item Model
    """
    class Meta:
        model = Item
        fields = '__all__'
