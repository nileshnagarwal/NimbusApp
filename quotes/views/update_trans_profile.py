"""
Update TransporterProfile based on the Quotations Received upto now
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from quotes.models import SupplierQuote
from masters.models import Places, TransporterProfile

from common.functions.shapefile import *

from pprint import pprint

# Create your views here
class UpdateTransProfile(generics.ListAPIView):
    """
    Update TransporterProfile based on the Quotations Received upto now
    """
    def get(self, request, *args, **kwargs):
        # Get all quotations
        quotations = SupplierQuote.objects.all()
        counter = 0
        for quotation in quotations:
            counter+=1
            # Get Enquiry Instance for the quotation
            enquiry = quotation.enquiry_id
            transporter_id = quotation.transporter_id
            src_places = enquiry.places.filter(src_dest__exact=Places.Source).\
                order_by('place_id')
            dest_places = enquiry.places.filter(src_dest__exact=Places.Destination).\
                order_by('place_id')
            vehicle_type_id = quotation.vehicle_type_id.all()
            source_id = []
            destination_id = []
            for place in src_places:
                if counter == 1:
                    print('Source place: ',place)
                    pprint(vars(place))
                if place.district_id is None:
                    district_id = point_in_polygon(place.lat, place.lng)
                    source_id.append(district_id)
                    print('source_id updated to: ', source_id)
                else:
                    source_id.append(place.district_id)
            for place in dest_places:
                if counter == 1:
                    print('Destination place: ',place)
                if place.district_id is None:
                    district_id = point_in_polygon(place.lat, place.lng)
                    destination_id.append(district_id)
                    print('destination_id updated to: ', destination_id)
                else:
                    destination_id.append(place.district_id)
            if counter == 1:
                print('Source ID list: ',source_id)
                print('Destination ID list: ',destination_id)
                print('Enquiry: ', enquiry)
                print('Transporter ID: ',transporter_id.transporter_id)
                print('src_places: ', src_places)
                print('dest_places: ', dest_places)
                print('vehicle_type_id: ', vehicle_type_id)
            trans_profile_ent = TransporterProfile(transporter_id=transporter_id)
            trans_profile_ent.save()
            trans_profile_ent.source_id = source_id
            trans_profile_ent.destination_id = destination_id
            trans_profile_ent.vehicle_type_id = vehicle_type_id
            trans_profile_ent.load_type = [1,2]
                # , destination_id=[1], \
                # vehicle_type_id=[1], load_type=[1])
            print('trans_profile_ent: ', trans_profile_ent)
            print('trans_profile_ent.trans_profile_id: ', trans_profile_ent.trans_profile_id)
            # Get Source and Destination District for the quotation
        return Response(None, status.HTTP_200_OK)

