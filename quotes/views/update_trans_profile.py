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
        UpdateTransProfile.update_trans_profile()
        return Response(None, status.HTTP_200_OK)

    @staticmethod
    def update_trans_profile():
        # Get all quotations
        quotations = SupplierQuote.objects.filter(linked_trans_profiles__isnull=True)
        for quotation in quotations:
            # Get Enquiry Instance for the quotation
            enquiry = quotation.enquiry_id
            # Get Transporter Instance for the quotation
            transporter_id = quotation.transporter_id
            # Create a TransporterProfile Instance and save to the DB
            trans_profile_ent = TransporterProfile(transporter_id=transporter_id, quote_id=quotation)
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
                if place.district_id is None:
                    # We need to send locality or admin_area_lvl_2 ie district name
                    # recvd from google to point_in_polygon method
                    if place.locality:
                        location = place.locality
                    else:
                        location = place.administrative_area_level_2
                    district_id = point_in_polygon(place.lat, place.lng, location=location)
                    district = District.objects.get(pk=district_id)
                    place.district_id = district
                    place.save()
                    source_id_arr.append(district)
                    trans_profile_ent.source_id.add(district)
                else:                    
                    source_id_arr.append(place.district_id)
                    trans_profile_ent.source_id.add(place.district_id)
            for place in dest_places: # Get district of all source places
                if place.district_id is None:
                    if place.locality:
                        location = place.locality
                    else:
                        location = place.administrative_area_level_2
                    district_id = point_in_polygon(place.lat, place.lng, location=location)
                    district = District.objects.get(pk=district_id)
                    place.district_id = district
                    place.save()
                    destination_id_arr.append(district)
                    trans_profile_ent.destination_id.add(district)
                else:
                    destination_id_arr.append(place.district_id)
                    trans_profile_ent.destination_id.add(place.district_id)
            # Get vehicle type queryset from the quotation
            vehicle_type_id = quotation.vehicle_type_id.all()
            for vehicle_type in vehicle_type_id:
                trans_profile_ent.vehicle_type_id.add(vehicle_type)
            trans_profile_ent.load_type.add(load_type)

