from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import VehicleBody, VehicleType, LoadType, Transporter, \
    ExtraExpenses, District, TransporterProfile
from .serializers import VehicleBodySerializer, VehicleTypeSerializer, \
    LoadTypeSerializer, TransporterSerializer, ExtraExpensesSerializer, Places, \
    PlacesSerializer, DistrictSerializer, TransporterProfileSerializer


# Create your views here.
class VehicleTypeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = VehicleType.objects.all().order_by('-vehicle')
    serializer_class = VehicleTypeSerializer
    pagination_class = None

class VehicleTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    pagination_class = None

class VehicleBodyList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = VehicleBody.objects.all().order_by('-vehicle_body_id')
    serializer_class = VehicleBodySerializer
    pagination_class = None

class VehicleBodyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleBody.objects.all()
    serializer_class = VehicleBodySerializer
    pagination_class = None

class LoadTypeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LoadType.objects.all().order_by('-load_type')
    serializer_class = LoadTypeSerializer
    pagination_class = None

class LoadTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoadType.objects.all()
    serializer_class = LoadTypeSerializer
    pagination_class = None

class TransporterList(generics.ListCreateAPIView):
    queryset = Transporter.objects.all().order_by('transporter')
    serializer_class = TransporterSerializer
    pagination_class = None

class TransporterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer
    pagination_class = None

class ExtraExpensesList(generics.ListCreateAPIView):
    queryset = ExtraExpenses.objects.all().order_by('extra_expenses')
    serializer_class = ExtraExpensesSerializer
    pagination_class = None

class ExtraExpensesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExtraExpenses.objects.all()
    serializer_class = ExtraExpensesSerializer
    pagination_class = None

class PlacesList(generics.ListCreateAPIView):
    """Creating List and Post functions for Places model"""
    queryset = Places.objects.all().order_by('place_id')
    serializer_class = PlacesSerializer
    pagination_class = None

class PlacesDetail(generics.RetrieveUpdateDestroyAPIView):
    """Creating RUD functions for Places model"""
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    pagination_class = None

class DistrictList(generics.ListCreateAPIView):
    """Creating List and Post functions for District model"""
    queryset = District.objects.all().order_by('district_id')
    serializer_class = DistrictSerializer
    pagination_class = None

class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    """Creating RUD functions for District model"""
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    pagination_class = None

class TransporterProfileList(generics.ListCreateAPIView):
    """Creating List and Post functions for District model"""
    queryset = TransporterProfile.objects.all().order_by('trans_profile_id')
    serializer_class = TransporterProfileSerializer
    pagination_class = None

class TransporterProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """Creating RUD functions for District model"""
    queryset = TransporterProfile.objects.all()
    serializer_class = TransporterProfileSerializer
    pagination_class = None
