"""
Serializers for the Quotes Module
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer)
from .models import User
# Defining serializers for common app

class UserSerializer(serializers.ModelSerializer):
    """
    Enquiry Model Serializer.
    """
    class Meta:
        model = User
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['name'] = user.get_full_name()
        token['user_type'] = user.user_type

        return token