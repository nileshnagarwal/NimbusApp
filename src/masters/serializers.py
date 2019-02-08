"""
Serializers for Masters Module
"""

from rest_framework import serializers
from masters.models import Vehicle_type, Vehicle_body, Transporter, Extra_expenses, Places
# Defining serializers for quotes app


class Vehicle_TypeSerializer(serializers.ModelSerializer):
    """
    Vehicle Type ModelSerializer.
    """
    class Meta:
        model = Vehicle_type
        fields = '__all__'

class Vehicle_BodySerializer(serializers.ModelSerializer):
    """
    Vehicle Body ModelSerializer.
    """
    class Meta:
        model = Vehicle_body
        fields = '__all__'

class TransporterSerializer(serializers.ModelSerializer):
    """
    Transporter ModelSerializer.
    """
    class Meta:
        model = Transporter
        fields = '__all__'

class Extra_ExpensesSerializer(serializers.ModelSerializer):
    """
    Extra Expenses ModelSerializer.
    """
    class Meta:
        model = Extra_expenses
        fields = '__all__'

class PlacesSerializer(serializers.ModelSerializer):
    """
    Places ModelSerializer.
    """
    class Meta:
        model = Places
        fields = '__all__'
