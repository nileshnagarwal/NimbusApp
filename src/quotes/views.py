from django.shortcuts import render
from quotes.models import Enquiry, SupplierQuote
from quotes.serializers import EnquirySerializer, SupplierQuoteSerializer
from rest_framework import generics

# Create your views here.
class EnquiryList(generics.ListCreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer


class EnquiryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer

class SupplierQuoteList(generics.ListCreateAPIView):
    queryset = SupplierQuote.objects.all()
    serializer_class = SupplierQuoteSerializer

class SupplierQuoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupplierQuote.objects.all()
    serializer_class = SupplierQuoteSerializer