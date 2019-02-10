"""
Views for the Quotes module.
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from quotes.models import Enquiry, SupplierQuote
from quotes.serializers import EnquirySerializer, SupplierQuoteSerializer
from masters.serializers import PlacesSerializer

# Create your views here.
class EnquiryList(generics.ListCreateAPIView):
    """
    This view gets enquiry data in request. This data also has the multiple sources and
    destinations as array of objects. We need to pop this out and pass it to the resp
    serializers.
    """
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer

    # Overriding the post() to handle creating the place
    def post(self, request, *args, **kwargs):
        # First we pop out the source, destination and return loc
        sources = request.data.pop("sources")
        destinations = request.data.pop("destinations")
        return_loc = request.data.pop("return")

        # Next we save the enquiry to get enquiry_id
        enq_serializer = EnquirySerializer(data=request.data)
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
                        return Response(enq_serializer.data, status.HTTP_201_CREATED)
                    return Response(return_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(destination_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(source_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(enq_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnquiryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic EnquiryDetail View
    """
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer

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
