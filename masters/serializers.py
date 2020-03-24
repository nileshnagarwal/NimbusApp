"""
Serializers for Masters Module
"""

from rest_framework import serializers
from .models import VehicleType, VehicleBody, LoadType, Transporter, \
    ExtraExpenses, Places, District, TransporterProfile, Client, ClientAddress
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

class LoadTypeSerializer(serializers.ModelSerializer):
    """
    Load Type ModelSerializer.
    """
    class Meta:
        model = LoadType
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

class DistrictSerializer(serializers.ModelSerializer):
    """
    District ModelSerializer.
    """
    neighbors_str = serializers.StringRelatedField(source='neighbors', many=True, read_only=True)

    class Meta:
        model = District
        fields = ('district_id', 'district', 'state', 'lat', \
            'lng', 'unique_id', 'neighbors', 'neighbors_str', )

class TransporterProfileSerializer(serializers.ModelSerializer):
    """
    TransporterProfile ModelSerializer.
    """
    class Meta:
        model = TransporterProfile
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    """
    Client ModelSerializer.
    """
    class Meta:
        model = Client
        fields = '__all__'

class ClientAddressSerializer(serializers.ModelSerializer):
    """
    ClientAddress ModelSerializer.
    """
    class Meta:
        model = ClientAddress
        fields = '__all__'
