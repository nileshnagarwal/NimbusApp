"""
Views for the Quotes module.
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import CursorPagination

from quotes.models import Enquiry, SupplierQuote
from quotes.serializers import (EnquiryDetailedSerializer, SupplierQuoteSerializer,
                                EnquirySerializer)
from quotes.views.update_trans_profile import UpdateTransProfile
from masters.serializers import PlacesSerializer
from masters.models import Places, VehicleType, LoadType
from fcm_django.models import FCMDevice
from common.models import User

from common.functions.haversine import haversine
from common.functions.shapefile import point_in_polygon
import datetime
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
    pagination_class = CursorPagination

    # Overriding the post() to handle creating the place
    def post(self, request, *args, **kwargs):
        # First we pop out the source, destination and return loc
        sources = request.data.pop("sources")
        destinations = request.data.pop("destinations")
        return_loc = request.data.pop("return", None)

        # Check if the enquiry is Unfloated Confirmed
        if Enquiry.UnfloatedEnquiry==request.data['status']:
            data_copy = request.data.copy()
            data_copy['cnf_enquiry_no'] = data_copy['enquiry_no']
            data_copy['cnf_loading_date'] = data_copy['loading_date']
            data_copy['cnf_comments'] = data_copy['comments']
            data_copy['cnf_created'] = datetime.now().isoformat()
            # Next we save the enquiry to get enquiry_id
            # If unfloated, save using data_copy else using request.data
            enq_serializer = EnquiryDetailedSerializer(data=data_copy)
        else:
            enq_serializer = EnquiryDetailedSerializer(data=request.data)
        
        if enq_serializer.is_valid():
            enquiry = enq_serializer.save()
            # Now we need to save the enquiry_id, src_dest and district
            # fields in source, destination and return
            for source in sources:
                source['enquiry_id'] = enquiry.enquiry_id
                source['src_dest'] = "Source"
                if source['locality']:
                        location = source['locality']
                else:
                    location = source['administrative_area_level_2']
                print(location)
                source['district_id'] = point_in_polygon(source['lat'], source['lng'], location=location)
            for destination in destinations:
                destination['enquiry_id'] = enquiry.enquiry_id
                destination['src_dest'] = "Destination"
                if destination['locality']:
                        location = destination['locality']
                else:
                    location = destination['administrative_area_level_2']
                print(location)
                destination['district_id'] = point_in_polygon(destination['lat'], destination['lng'], location=location)
            return_loc['enquiry_id'] = enquiry.enquiry_id
            return_loc['src_dest'] = "Return"
            if not (return_loc['lat'] in [None, ''] or return_loc['lng'] in [None, '']):
                if return_loc['locality']:
                        location = return_loc['locality']
                else:
                    location = return_loc['administrative_area_level_2']
                print(location)
                return_loc['district_id'] = point_in_polygon(return_loc['lat'], return_loc['lng'], location=location)

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

class ConfirmEnquiry(generics.UpdateAPIView):
    """
    Confirm Floated Enquiry by providing all the required fields
    """
    queryset = Enquiry.objects.all()
    serializer_class = EnquiryDetailedSerializer

    def patch(self, request, *args, **kwargs):
        # Get access to the instance that is being confirmed
        instance = self.get_object()
        # Check if already confirmed
        if instance.cnf_loading_date == None:
            # Create a dict with the confirmation data that needs to be patched
            cnf = {}
            cnf['data'] = request.data.copy()
            cnf['data']['cnf_enquiry_no'] = "C" + instance.enquiry_no[1:]
            cnf['data']['cnf_created'] = datetime.now().isoformat() 
            cnf['data']['status'] = Enquiry.FinalisedOrder
            # partial=True allows serializer.isvalid without sharing all
            # mandatory data
            serializer = EnquirySerializer(instance,data=cnf['data'], \
                partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        # If already confirmed, return error
        else:
            return Response({'error': 'Enquiry is already confirmed'}, status.HTTP_409_CONFLICT)


class EnquirySearchList(generics.ListAPIView):
    """
    Search Enquiries based on criteria
    """
    
    serializer_class = EnquiryDetailedSerializer
    pagination_class = CursorPagination

    @staticmethod
    def filter_date_status(qs, status, from_date, to_date):
        """
        Function takes a qs to be filtered and acc to the status received, it decides
        if loading_date is to be used for filtering or cnf_loading_date is to be used.
        """
        if Enquiry.FinalisedOrder in status:
            return qs.filter(cnf_loading_date__gte=from_date, \
                cnf_loading_date__lte=to_date, status__exact=status).distinct() \
                .order_by('-enquiry_id')
        elif Enquiry.UnfloatedEnquiry in status:
            return qs.filter(cnf_loading_date__gte=from_date, \
                cnf_loading_date__lte=to_date, status__exact=status).distinct() \
                .order_by('-enquiry_id')
        elif Enquiry.FloatedEnquiry in status:
            return qs.filter(loading_date__gte=from_date, \
                loading_date__lte=to_date, status__exact=status).distinct() \
                .order_by('-enquiry_id')


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
        
        # Get status from query params
        status = self.request.query_params.get('status', None)        

        # Get source data from query params
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
        
        # Get destination data from query params
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
        
        # Filter the queryset using vehicle_type, source and destination
        qs = Enquiry.objects.filter(vehicle_type__in=vehicle_type, \
            enquiry_id__in=enq_ids).distinct().order_by('-enquiry_id')

        # For filtering according to status, we need to check the status
        # and accordingly apply filters to loading_date or cnf_loading_date
        # qs_arr is used for storing all querysets for various status options
        qs_arr = []
        # status_arr is used to store the possible status options
        status_arr = []
        
        # Check if we've received blank status value
        if status is None or status.isspace():
            # If yes we store all possible status values in status_arr
            for a, b in Enquiry._status_choices:
                status_arr.append(a)        
        else:
            # Else we store the status value received
            status_arr.append(status)
        
        # Next we call the filter_date_status function to filter data
        # acc to the status values to be filtered
        for i, status in enumerate(status_arr):
            qs_arr.append(EnquirySearchList.filter_date_status(qs, status,\
                from_date, to_date))
        
        # We combine the querysets to create the final queryset
        qs_final = Enquiry.objects.none() # Create blank queryset
        for qs_part in qs_arr:
            qs_final = qs_final | qs_part # | is used to combine querysets
        
        # .distinct() helps to avoid duplicates in our queryset
        # Refer: https://stackoverflow.com/a/38452675/3608786
        return qs_final.distinct()

class SupplierQuoteList(generics.ListCreateAPIView):
    """
    Generic Supplier Quote List and Create View
    """
    queryset = SupplierQuote.objects.all().order_by('-created')
    serializer_class = SupplierQuoteSerializer

    def get(self, request, *args, **kwargs):
        # Get user_type from request
        user_type = request.user.user_type
        # If user is developers, admin or sales person, show quotes from all users
        if user_type==User.developer or user_type==User.admin or user_type==User.sales:
            quotes = SupplierQuote.objects.all().order_by('-quote_id') 
        # Else show quotes from themselves only
        else:
            quotes = SupplierQuote.objects.filter(user_id__exact=request.user.id)\
                .order_by('-quote_id')
        # When serializing a list of objects, add many=True
        serializer = SupplierQuoteSerializer(quotes, many=True)
        return Response(serializer.data)

    # Overriding Post method to save transporter profile after
    # saving the quotation
    def post(self, request, *args, **kwargs):
        # Saving the quotation calling super post method
        response = super().post(request, *args, **kwargs)
        # Saving transporter profile
        UpdateTransProfile.update_trans_profile()
        return Response(response.data, status.HTTP_201_CREATED)

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
        # Get user_type from request
        user_type = request.user.user_type
        # If user is developers, admin or sales person, show quotes from all users
        if user_type==User.developer or user_type==User.admin or user_type==User.sales:
            quotes = SupplierQuote.objects.filter(enquiry_id=self.kwargs['pk'])   
        # Else show quotes from themselves only
        else:
            quotes = SupplierQuote.objects.filter(enquiry_id=self.kwargs['pk'], \
            user_id__exact=request.user.id)
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
    load_type = LoadType.objects.get(pk=enquiry['load_type_new'])
    body = source + ' to ' + destination + '. ' + str(load_type) + \
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