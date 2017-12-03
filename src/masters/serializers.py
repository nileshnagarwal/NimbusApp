from rest_framework import serializers
from masters.models import Vehicle_type, Vehicle_body, Transporter
# Defining serializers for quotes app


class Vehicle_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle_type
        fields = '__all__'

class Vehicle_BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle_body
        fields = '__all__'

class TransporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporter
        fields = '__all__'
