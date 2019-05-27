"""
Serializers for the Common Module
"""
from django.utils.six import text_type

from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer)
from .models import User
from fcm_django.models import FCMDevice
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
    
    def validate(self, attrs):        
        data = super(TokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh_token'] = text_type(refresh)
        data['access_token'] = text_type(refresh.access_token)

        return {"token": data}

class FCMDevicesSerializer(serializers.ModelSerializer):
    """
    Custom FCMDevices Serializer
    """
    user = UserSerializer()

    class Meta:
        model = FCMDevice
        fields = ('registration_id', 'name', 'active', 'user',
                    'device_id', 'type')