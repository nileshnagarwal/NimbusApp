"""
Serializers for Masters Module
"""

from rest_framework import serializers
from masters.models import VehicleType, VehicleBody, Transporter, ExtraExpenses, Places
# Defining serializers for quotes app


class VehicleTypeSerializer(serializers.ModelSerializer):
    """
    Vehicle Type ModelSerializer.
    """
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleBodySerializer(serializers.ModelSerializer):
    """
    Vehicle Body ModelSerializer.
    """
    class Meta:
        model = VehicleBody
        fields = '__all__'

class TransporterSerializer(serializers.ModelSerializer):
    """
    Transporter ModelSerializer.
    """
    class Meta:
        model = Transporter
        fields = '__all__'

class ExtraExpensesSerializer(serializers.ModelSerializer):
    """
    Extra Expenses ModelSerializer.
    """
    class Meta:
        model = ExtraExpenses
        fields = '__all__'

class PlacesSerializer(serializers.ModelSerializer):
    """
    Places ModelSerializer.
    """
    class Meta:
        model = Places
        fields = '__all__'
