from django.shortcuts import render
from masters.models import Vehicle_body, Vehicle_type, Transporter
from masters.serializers import Vehicle_BodySerializer, Vehicle_TypeSerializer, TransporterSerializer
from rest_framework import generics

# Create your views here.
class Vehicle_TypeList(generics.ListCreateAPIView):
    queryset = Vehicle_type.objects.all().order_by('-vehicle_type_id')
    serializer_class = Vehicle_TypeSerializer


class Vehicle_TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle_type.objects.all()
    serializer_class = Vehicle_TypeSerializer

class Vehicle_BodyList(generics.ListCreateAPIView):
    queryset = Vehicle_body.objects.all().order_by('-vehicle_body_id')
    serializer_class = Vehicle_BodySerializer


class Vehicle_BodyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle_body.objects.all()
    serializer_class = Vehicle_BodySerializer

class TransporterList(generics.ListCreateAPIView):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer


class TransporterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer