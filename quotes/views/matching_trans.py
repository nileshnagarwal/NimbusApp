"""
Search suitable Transporters based on enquiry
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from quotes.models import Enquiry
from masters.models import Places, TransporterProfile, Transporter, District
from masters.serializers import TransporterSerializer

# Create your views here

class MatchingTrans(generics.ListAPIView):
    """
    Get enquiry and search criteria from front end and return the
    mathing transporters for the given enquiry
    """
    def get(self, request, *args, **kwargs):
        # Extract level and enquiry_id from query
        source_level = int(request.query_params.get('source_level', 0))
        dest_level = int(request.query_params.get('dest_level', 0))
        enquiry_id = request.query_params.get('enquiry_id')

        # Get enquiry instance
        enquiry = Enquiry.objects.get(enquiry_id__exact=enquiry_id)

        # Get source_places as the first source place instance. This is to handle
        # cases where we have multi point loading/unloading.
        source_places = enquiry.places.filter(src_dest__exact=Places.Source).\
            order_by('place_id').first()
        # Get dest_places as the last destination place instance
        dest_places = enquiry.places.filter(src_dest__exact=Places.Destination).\
            order_by('place_id').last()
        
        # Get district instance from source and dest
        source_district = source_places.district_id
        dest_district = dest_places.district_id

        # Get neighbors districts from get_neighbors function
        districts = MatchingTrans.get_neighbors(source_district, source_level, \
            dest_district, dest_level)

        # Get matching trans from get_matching_transporters function
        filtered_trans = MatchingTrans.get_matching_transporters(enquiry_id, \
            districts['source_districts'], districts['dest_districts'])

        # Return result
        return Response(filtered_trans.data, status.HTTP_200_OK)
    
    @staticmethod
    def get_neighbors(source_district, source_level, dest_district, dest_level):
        """
        Get src and dest district and level and accoringly call the get_neighbors by level
        for each src as well as dest. Return the combined result.
        """
        source_districts = MatchingTrans.get_neighbors_by_level(source_level, source_district)
        dest_districts = MatchingTrans.get_neighbors_by_level(dest_level, dest_district)
        return {'source_districts': source_districts, 'dest_districts': dest_districts}

    @staticmethod
    def get_neighbors_by_level(level, district):
        """
        Return the neighbors of the input district depending on the level
        received as input. Level 0 means the same district is returned. 
        Level 1 means the immediate neighbors of the district are returned.
        Level 2 means the nerighbors of the immediate neighbors are also returned.
        Level 2 is max. The result is returned as queryset of the districts.        
        """
        if level > 2:
            level = 2 # Max level allowed is 2
        
        # Define districts as qs
        districts = District.objects.none()
        
        if level == 0:
            # return qs containing the same district as input
            districts = District.objects.filter(pk=district.district_id)

        elif level == 1:
            # return qs containing immediate neighbors of the input district
            districts = district.neighbors.all()

        elif level == 2:
            # return qs containing neighbors of immediate neigbors of input 
            # district
            # First get immediate neighbors.
            neighbors = district.neighbors.all()
            # For each neighbor get its neighbors and add to the queryset.
            for neighbor in neighbors:
                districts = districts.union(neighbor.neighbors.all())
        
        return districts

    @staticmethod
    def get_matching_transporters(enquiry_id, src_places, dest_places):
        """
        Find transporters matching the load_type, vehicle_type and source,
        destination criteria and return the serializer of matching Transporters.
        """
        # First get enquiry instance
        enquiry = Enquiry.objects.get(enquiry_id__exact=enquiry_id)
        # From enquiry, get load_type and vehicle_type
        load_type = enquiry.load_type_new
        vehicle_type = enquiry.vehicle_type.all()

        # Now we'll filter for transporters providing transportation from 
        # the list of source and destination (list received may include nerighbors).
        # This step will be done in 2 steps. First we'll filter considering the source
        # of transporter matches the source districts and destination matches the destination
        # districts. Then we'll reverse the case with source matching destination districts and
        # destination matching source districts.

        # First defining Q objects for enquiry source and destination matching transporter profile
        # source and destination resp
        q_source_source = Q(source_id__in=src_places.values('district_id'))
        q_dest_dest = Q(destination_id__in=dest_places.values('district_id'))

        # Second defining Q objects for enquiry destination and source matching transporter profile
        # source and destination resp
        q_dest_source = Q(destination_id__in=src_places.values('district_id'))
        q_source_dest = Q(source_id__in=dest_places.values('district_id'))

        # Finally defining Q objects for vehicle type and load type 
        q_vehicle_type = Q(vehicle_type_id__in=vehicle_type.values('vehicle_type_id'))
        q_load_type = Q(load_type__exact=load_type)

        # Combining Q objects in a chain. & stands for AND operator and | stands for OR operator. 
        # Refer https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q
        filtered_trans = TransporterProfile.objects.filter((q_source_source & q_dest_dest) | (q_dest_source & q_source_dest))\
                            .filter(q_vehicle_type).filter(q_load_type)               

        # Get Transporter Queryset from filtered_trans Queryset
        filtered_trans_qs = Transporter.objects.filter(trans_profile__in=filtered_trans).distinct()
        # Serialize the qs
        filtered_trans = TransporterSerializer(filtered_trans_qs, many=True)
        # Return the serialized qs
        return filtered_trans
