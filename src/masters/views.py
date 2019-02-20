from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import VehicleBody, VehicleType, Transporter, ExtraExpenses
from .serializers import VehicleBodySerializer, VehicleTypeSerializer, TransporterSerializer, ExtraExpensesSerializer, Places, PlacesSerializer


# Create your views here.
class VehicleTypeList(generics.ListCreateAPIView):
    queryset = VehicleType.objects.all().order_by('-vehicle_type_id')
    serializer_class = VehicleTypeSerializer


class VehicleTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer

class VehicleBodyList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = VehicleBody.objects.all().order_by('-vehicle_body_id')
    serializer_class = VehicleBodySerializer

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)

class VehicleBodyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleBody.objects.all()
    serializer_class = VehicleBodySerializer

class TransporterList(generics.ListCreateAPIView):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer

class TransporterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer

class ExtraExpensesList(generics.ListCreateAPIView):
    queryset = ExtraExpenses.objects.all()
    serializer_class = ExtraExpensesSerializer

class ExtraExpensesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExtraExpenses.objects.all()
    serializer_class = ExtraExpensesSerializer

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
