"""
Serializers for the Quotes Module
"""
from rest_framework import serializers
from .models import User
# Defining serializers for common app

class UserSerializer(serializers.ModelSerializer):
    """
    Enquiry Model Serializer.
    """
    class Meta:
        model = User
        fields = '__all__'