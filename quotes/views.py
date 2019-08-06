"""
Views for the Quotes module.
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from quotes.models import Enquiry, SupplierQuote, ConfirmEnquiry
from quotes.serializers import (EnquiryDetailedSerializer, SupplierQuoteSerializer,
                                ConfirmEnquirySerializer, EnquirySerializer)
from masters.serializers import PlacesSerializer
from masters.models import Places, VehicleType
from fcm_django.models import FCMDevice
from common.models import User

from common.functions.haversine import haversine

from datetime import datetime, timedelta
import pytz # Imported to set Timezone
import dateutil.parser
from decimal import Decimal

# Create your views here.
class EnquiryList(generics.ListCreateAPIView):
    """
    This view gets enquiry data in request. This data also has the multiple sources
    and destinations as array of objects. We need to pop this out and pass it to
    the resp serializers.
    """
    queryset = Enquiry.objects.all().order_by('-created', 'enquiry_no')
    serializer_class = EnquiryDetailedSerializer

    # Overriding the post() to handle creating the place
    def post(self, request, *args, **kwargs):
        # First we pop out the source, destination and return loc
        sources = request.data.pop("sources")
        destinations = request.data.pop("destinations")
        return_loc = request.data.pop("return")

        # Next we save the enquiry to get enquiry_id
        enq_serializer = EnquiryDetailedSerializer(data=request.data)
        if enq_serializer.is_valid():
            enquiry = enq_serializer.save()
            # Now we need to save the enquiry_id and src_dest in
            # source, destination and return
            for source in sources:
                source['enquiry_id'] = enquiry.enquiry_id
                source['src_dest'] = "Source"
            for destination in destinations:
                destination['enquiry_id'] = enquiry.enquiry_id
                destination['src_dest'] = "Destination"
            return_loc['enquiry_id'] = enquiry.enquiry_id
            return_loc['src_dest'] = "Return"

            # Finally we save source, destination and return
            # Since we are creating many sources together, we need to add
            # flag many=true while instantiating the serializer.
            source_serializer = PlacesSerializer(data=sources, many=True)
            destination_serializer = PlacesSerializer(data=destinations, many=True)
            return_serializer = PlacesSerializer(data=return_loc)
            if source_serializer.is_valid():
                if destination_serializer.is_valid():
                    if return_serializer.is_valid():
                        source_serializer.save()
                        destination_serializer.save()
                        return_serializer.save()
                        send_enq_notification(request.data, enquiry.enquiry_id, \
                            sources, destinations)
                        return Response(enq_serializer.data, status.HTTP_201_CREATED)
                    source_serializer.save()
                    destination_serializer.save()
                    send_enq_notification(request.data, enquiry.enquiry_id, sources,\
                        destinations)
                    return Response(enq_serializer.data, status.HTTP_201_CREATED)
                return Response(destination_serializer.errors, \
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(source_serializer.errors, \
                status=status.HTTP_400_BAD_REQUEST)
        return Response(enq_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnquiryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic EnquiryDetail View
    """
    queryset = Enquiry.objects.all()
    serializer_class = EnquiryDetailedSerializer

class EnquirySearchList(generics.ListAPIView):
    """
    Search Enquiries based on criteria
    """
    
    serializer_class = EnquiryDetailedSerializer

    def get_queryset(self):
        """
        Overrides get_queryset function to search enquiries based on
        criteria received and returns the filtered enquiries.
        """
        # First store the data received in request in local variables
        
        std_from_date = datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)
        std_to_date = datetime(2100, 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)
        from_date = self.request.query_params.get('from_date', std_from_date)
        to_date = self.request.query_params.get('to_date', std_to_date)            
        # Change date from str to datetime
        if from_date != std_from_date:
            from_date = dateutil.parser.parse(from_date)
        if to_date != std_to_date:
            to_date = dateutil.parser.parse(to_date)
        
        vehicle_type = self.request.query_params.get('vehicle_type', None)
        # Change vehicle_type from str to int array
        if vehicle_type is not None:
            vehicle_type = [int(x.strip()) for x in \
                            vehicle_type.strip('[]').split(',') if x]
            if vehicle_type.__len__()== 0:
                # If vehicle_type is blank array, get all vehicle types
                vehicle_type = VehicleType.objects.all().\
                    values_list('vehicle_type_id', flat=True)
        if vehicle_type is None:
                # If vehicle_type was not received, get all vehicle types
                vehicle_type = VehicleType.objects.all().\
                    values_list('vehicle_type_id', flat=True)
        
        status = self.request.query_params.get('status', None)        

        source_lat = self.request.query_params.get('source_lat', None)
        source_lng = self.request.query_params.get('source_lng', None)
        source_rad = self.request.query_params.get('source_rad', None)
        if (source_lat and source_lng and source_rad is not None):
            # Change lat, long from str to decimal
            source_lat = Decimal(source_lat.strip())
            source_lng = Decimal(source_lng.strip())
            source_rad = Decimal(source_rad.strip())
            # First we will filter for location        
            # Get source places
            source_places = Places.objects.filter(src_dest__exact='Source')
            # Local variable to store array of enquiry_ids of enquiries having
            # matching source destination criteria
            enq_ids = []
            # Filter out the source places that match criteria
            # Looping through the source_places, we check for criteria and save
            # enquiry_id of places that pass the criteria
            for place in source_places:
                if (haversine(source_lat, source_lng, place.lat, place.lng)) \
                    < source_rad:
                    if not place.enquiry_id.enquiry_id in enq_ids:
                        enq_ids.append(place.enquiry_id.enquiry_id)
            
        else:
            # If source criteria is not provided, enq_ids will contain all enquiries
            enq_ids = list(Enquiry.objects.all().values_list('enquiry_id', flat=True))        
        
        dest_lat = self.request.query_params.get('dest_lat', None)
        dest_lng = self.request.query_params.get('dest_lng', None)
        dest_rad = self.request.query_params.get('dest_rad', None)
        if (dest_lat and dest_lng and dest_rad is not None):
            dest_lat = Decimal(dest_lat.strip())
            dest_lng = Decimal(dest_lng.strip())
            dest_rad = Decimal(dest_rad.strip())
            # Filter out the destination places that match criteria
            # Looping through the destination places, we remove the enquiry_ids
            # of plaaces that fail the criteria
            dest_places = Places.objects.filter(enquiry_id__in=enq_ids, \
                            src_dest__exact='Destination')
            for place in dest_places:
                if (haversine(dest_lat, dest_lng, place.lat, place.lng)) \
                    > dest_rad:
                    if place.enquiry_id.enquiry_id in enq_ids:
                        enq_ids.remove(place.enquiry_id.enquiry_id)
                else:                
                    enq_ids.append(place.enquiry_id.enquiry_id)
                    
        # Finally apply all the filters to Enquiry Model Manager
        # .distinct() helps to avoid duplicates in our queryset
        # Refer: https://stackoverflow.com/a/38452675/3608786        
        if status is not None or '':
            qs = Enquiry.objects.filter(loading_date__gte=from_date, \
                loading_date__lte=to_date, vehicle_type__in=vehicle_type, \
                status__exact=status, enquiry_id__in=enq_ids).distinct()\
                .order_by('-enquiry_id')
        else:
            qs = Enquiry.objects.filter(loading_date__gte=from_date, \
                loading_date__lte=to_date, vehicle_type__in=vehicle_type, \
                enquiry_id__in=enq_ids).distinct().order_by('-enquiry_id')
        return qs

class ConfirmEnquiryList(generics.ListCreateAPIView):
    """
    Generic Confirm Enquiry List and Create View
    """
    queryset = ConfirmEnquiry.objects.all().order_by('-created')
    serializer_class = ConfirmEnquirySerializer

    def post(self, request, *args, **kwargs):
        """
        Override Post to convert the original enquiry_no from F* to C*
        """
        # request.data is immutable Dict. To make it mutable, we must use .copy()
        # Refer: https://docs.djangoproject.com/en/dev/ref/
        # request-response/#django.http.QueryDict
        con_enquiry_data = request.data.copy()
        original_enq = Enquiry.objects.get(enquiry_id=request.data['enquiry_id'])
        enq_ser = EnquirySerializer(original_enq)
        enquiry_no = enq_ser.data['enquiry_no']
        # Fast Method to edit a section of a string
        enquiry_no = "C" + enquiry_no[1:]
        con_enquiry_data['enquiry_no'] = enquiry_no
        con_enquiry_ser = ConfirmEnquirySerializer(data=con_enquiry_data)
        if con_enquiry_ser.is_valid():
            con_enquiry = con_enquiry_ser.save()
            return Response(con_enquiry_ser.data, status.HTTP_201_CREATED)
        return Response(con_enquiry_ser.errors, status.HTTP_400_BAD_REQUEST)

class ConfirmEnquiryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic Confirm Enquiry Detail View, Update and Delete
    """
    queryset = ConfirmEnquiry.objects.all()
    serializer_class = ConfirmEnquirySerializer

class ConfirmEnquiryCompleteList(generics.ListAPIView):
    """
    Confirm Enquiry Combined List from Enquiry and ComfirmEnquiry Models
    """
    queryset = ConfirmEnquiry.objects.all().order_by('-created')
    serializer_class = ConfirmEnquirySerializer

    def get(self, request, *args, **kwargs):
        """
        Override get to list all confirmed enquiries from Enquiry and ConfirmEnquiry
        Models
        """
        enq_qs = Enquiry.objects.filter(status='Confirmed Order').order_by('-created')
        con_enq_qs = ConfirmEnquiry.objects.all().order_by('-created')
        enquiry_ser = EnquiryDetailedSerializer(enq_qs, many=True)
        con_enq_ser = ConfirmEnquirySerializer(con_enq_qs, many=True)
        return Response({
            'direct_confirmed_orders': enquiry_ser.data,
            'convert_confirmed_orders': enquiry_ser.data
        })

class SupplierQuoteList(generics.ListCreateAPIView):
    """
    Generic Supplier Quote List and Create View
    """
    queryset = SupplierQuote.objects.all().order_by('-created')
    serializer_class = SupplierQuoteSerializer

class SupplierQuoteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic EnquiryDetail View
    """
    queryset = SupplierQuote.objects.all()
    serializer_class = SupplierQuoteSerializer

class SupplierQuotesForEnquiry(generics.ListCreateAPIView):
    """
    Generic EnquiryDetail View
    """
    queryset = SupplierQuote.objects.all().order_by('-created')
    serializer_class = SupplierQuoteSerializer

    def get(self, request, pk, *args, **kwargs):
        quotes = SupplierQuote.objects.filter(enquiry_id=self.kwargs['pk'])
        # When serializing a list of objects, add many=True
        serializer = SupplierQuoteSerializer(quotes, many=True)
        return Response(serializer.data)

def send_enq_notification(enquiry, enquiry_id, sources, destinations):
    """
    Send push notifications using fcm_django to Traffic Incharge
    when a new enquiry has been posted.
    Refer: https://github.com/xtrinch/fcm-django
    """
    # The notification type that we will be using is notification with data
    """
    {
    "to" : "bk3RNwTe3H0:CI2k_HHwgIpoDKCIZvvDMExUdFQ3P1...",
    "notification" : {
      "body" : "great match!",
      "title" : "Portugal vs. Denmark",
      "icon" : "myicon"
    }
    "data" : {
      "Nick" : "Mario",
      "Room" : "PortugalVSDenmark"
    }
    """
    """
    To understand queryset filtering
    Refer: https://docs.djangoproject.com/en/dev/topics/db/queries/
    #lookups-that-span-relationships
    """
    # user_type 4 belongs to traffic incharge
    queryset = FCMDevice.objects.filter(user__user_type=4)
    datetime_object = datetime.strptime(enquiry['loading_date'], '%Y-%m-%dT%H:%M:%S.%fZ') \
        + timedelta(minutes=330)
    source = trimPlaceStr(sources[0]['place'])
    destination = trimPlaceStr(destinations[0]['place'])
    title = 'New Enquiry Added. #' + enquiry['enquiry_no']
    body = source + ' to ' + destination + '. ' + enquiry['load_type'] + \
        ' Cargo. Loading on ' + datetime_object.strftime("%d %b, %Y | %a")
    queryset.send_message(title=title, body=body, data={"enquiry_id": enquiry_id})

def trimPlaceStr(place):
    """
    Triming Place Name str for push notifications.
    If place name has 2 or more commas, we take the
    part before the second comma. If not we trim for any
    spaces and return the string.
    """
    placeArr = place.split(',')
    if(place.count(',')>1):
        return ((placeArr[0].strip() + ', ' + placeArr[1].strip()))
    else:
        return place.strip()