"""
Update TransporterProfile based on the Quotations Received upto now
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from quotes.models import SupplierQuote
from masters.models import Places, TransporterProfile, District, VehicleType

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
            # Get Transporter Instance for the quotation
            transporter_id = quotation.transporter_id
            # Create a TransporterProfile Instance and save to the DB
            trans_profile_ent = TransporterProfile(transporter_id=transporter_id)
            trans_profile_ent.save()
            # Get source and dest places queryset from the enquiry
            src_places = enquiry.places.filter(src_dest__exact=Places.Source).\
                order_by('place_id')
            dest_places = enquiry.places.filter(src_dest__exact=Places.Destination).\
                order_by('place_id')            
            # Get load type from enquiry
            load_type = enquiry.load_type_new
            # Get Source and Destination Districts from Places in Enquiry
            source_id_arr = [] # Store district ids of source
            destination_id_arr = [] # Store district ids of destination
            for place in src_places: # Get district of all source places
                if counter == 1:
                    print('Source place: ',place)
                    pprint(vars(place))
                if place.district_id is None:
                    district_id = point_in_polygon(place.lat, place.lng)
                    district = District.objects.get(pk=district_id)
                    source_id_arr.append(district)
                    trans_profile_ent.source_id.add(district)
                    print('source_id updated to: ', source_id_arr)
                else:                    
                    source_id_arr.append(place.district_id)
                    trans_profile_ent.source_id.add(place.district_id)
            for place in dest_places: # Get district of all source places
                if counter == 1:
                    print('Destination place: ',place)
                if place.district_id is None:
                    district_id = point_in_polygon(place.lat, place.lng)
                    district = District.objects.get(pk=district_id)
                    destination_id_arr.append(district)
                    trans_profile_ent.destination_id.add(district)
                    print('destination_id updated to: ', destination_id_arr)
                else:
                    destination_id_arr.append(place.district_id)
                    trans_profile_ent.destination_id.add(place.district_id)
            # Get vehicle type queryset from the quotation
            vehicle_type_id = quotation.vehicle_type_id.all()
            for vehicle_type in vehicle_type_id:
                trans_profile_ent.vehicle_type_id.add(vehicle_type)
            if counter == 1:
                print('Source ID list: ',source_id_arr)
                print('Destination ID list: ',destination_id_arr)
                print('Enquiry: ', enquiry)
                print('Transporter ID: ',transporter_id.transporter_id)
                print('src_places: ', src_places)
                print('dest_places: ', dest_places)
                print('vehicle_type_id: ', vehicle_type_id)
                print('load_type: ', load_type)
            trans_profile_ent.load_type.add(load_type)
            print('trans_profile_ent: ', trans_profile_ent)
            print('trans_profile_ent.trans_profile_id: ', trans_profile_ent.trans_profile_id)
        return Response(None, status.HTTP_200_OK)

