"""
Views for the Quotes module.
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from quotes.models import Enquiry, SupplierQuote
from quotes.serializers import EnquiryDetailedSerializer, SupplierQuoteSerializer
from masters.serializers import PlacesSerializer
from fcm_django.models import FCMDevice
from common.models import User

from datetime import datetime, timedelta

# Create your views here.
class EnquiryList(generics.ListCreateAPIView):
    """
    This view gets enquiry data in request. This data also has the multiple sources and
    destinations as array of objects. We need to pop this out and pass it to the resp
    serializers.
    """
    queryset = Enquiry.objects.all()
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
                        send_enq_notification(request.data, enquiry.enquiry_id, sources, destinations)
                        return Response(enq_serializer.data, status.HTTP_201_CREATED)
                    source_serializer.save()
                    destination_serializer.save()
                    send_enq_notification(request.data, enquiry.enquiry_id, sources, destinations)
                    return Response(enq_serializer.data, status.HTTP_201_CREATED)
                return Response(destination_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(source_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(enq_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnquiryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic EnquiryDetail View
    """
    queryset = Enquiry.objects.all()
    serializer_class = EnquiryDetailedSerializer

class SupplierQuoteList(generics.ListCreateAPIView):
    """
    Generic Supplier Quote List and Create View
    """
    queryset = SupplierQuote.objects.all()
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
    queryset = SupplierQuote.objects.all()
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