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
        fields = ('lr_no', 'client_id', 'vehicle_no', 'client')

class LorryReceiptSerializer(serializers.ModelSerializer):
    """
    Model Serializer for LorryReceipt Model
    """
    class Meta:
        model = LorryReceipt
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Item Model
    """
    class Meta:
        model = Item
        fields = '__all__'
