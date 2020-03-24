"""
Serializers for Operations Module
"""

from rest_framework import serializers
from .models import LorryReceipt, LorryReceiptNo, Item

class LorryReceiptNoSerializer(serializers.ModelSerializer):
    """
    Model Serializer for LorryReceiptNo Model
    """
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

class ItemSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Item Model
    """
    class Meta:
        model = Item
        fields = '__all__'
