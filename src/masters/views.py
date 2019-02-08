from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from masters.models import Vehicle_body, Vehicle_type, Transporter, Extra_expenses
from masters.serializers import Vehicle_BodySerializer, Vehicle_TypeSerializer, TransporterSerializer, Extra_ExpensesSerializer, Places, PlacesSerializer


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

class Extra_ExpensesList(generics.ListCreateAPIView):
    queryset = Extra_expenses.objects.all()
    serializer_class = Extra_ExpensesSerializer

class Extra_ExpensesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Extra_expenses.objects.all()
    serializer_class = Extra_ExpensesSerializer

class PlacesList(generics.ListCreateAPIView):
    """Creating List and Post functions for Places model"""
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.DATA, many=True)
    #     if serializer.is_valid():
    #         print("Serializer is Valid")
    #         print("Serializer Value is ", repr(serializer.data))
    #         serializer.save()
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED,
    #                         headers=headers)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def get_serializer(self, instance=None, data=None,
    #                 files=None, many=True, partial=False):
    #     return super(PlacesList, self).get_serializer(instance, data, files,
    #                                                 many, partial)

class PlacesDetail(generics.RetrieveUpdateDestroyAPIView):
    """Creating RUD functions for Places model"""
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
