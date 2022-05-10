"""
Serializers for Operations Module
"""

from rest_framework import serializers
from .models import LorryReceipt, LorryReceiptNo, Item
from masters.serializers import ClientAddressSerializer, ClientSerializer

class LorryReceiptNoSerializer(serializers.ModelSerializer):
    """
    Model Serializer for LorryReceiptNo Model
    """
    client = ClientSerializer(source='client_id', read_only=True)

    class Meta:
        model = LorryReceiptNo
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Item Model
    """
    class Meta:
        model = Item
        fields = '__all__'

class LorryReceiptSerializer(serializers.ModelSerializer):
    """
    Model Serializer for LorryReceipt Model
    """

    consignor_obj = ClientAddressSerializer(source='consignor_id', read_only=True)
    consignee_obj = ClientAddressSerializer(source='consignee_id', read_only=True)
    lr_obj = LorryReceiptNoSerializer(source='lr_no_id', read_only=True)
    items = ItemSerializer(source='item', many=True, read_only=True)

    class Meta:
        model = LorryReceipt
        fields = '__all__'

    # to_internal_value converts the value to avoid validation error
    # Without this we get error saying weight should be an integer
    # despite having null=True and default=0. Same for expiry date.
    def to_internal_value(self, data):
        if data.get('weight') == '':
            data['weight'] = 0.0
       
        return super(LorryReceiptSerializer, self).to_internal_value(data)

class LorryVerifySerializer(serializers.ModelSerializer):
    """
    Model Serializer for LR Verification
    """

    class Meta:
        model = LorryReceipt
        fields = ('lr_no_id', 'date', 'dispatch_from', 'ship_to', 'invoice_no', \
            'invoice_date', 'vehicle_no', 'boe_no', 'boe_date', 'dc_no', \
            'dc_date', 'ewaybill_no')