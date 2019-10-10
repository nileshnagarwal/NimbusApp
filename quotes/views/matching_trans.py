"""
Search suitable Transporters based on enquiry
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

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

        # Source matching Source districts and Destination matching Destination Districts
        filtered_trans_1 = TransporterProfile.objects.filter(source_id__in=src_places.values('district_id'))
        filtered_trans_1 = filtered_trans_1.filter(destination_id__in=dest_places.values('district_id'))

        # If we get 0 transporters from last filter, we'll have to convert the result to queryset
        # to keep consistency. All our filtered_tran will be querysets.
        if filtered_trans_1.count() == 0:
            filtered_trans_1 = TransporterProfile.objects.none()
        
        # Source matching Destination districts and Destination matching Source Districts
        filtered_trans_2 = TransporterProfile.objects.filter(destination_id__in=src_places.values('district_id'))
        filtered_trans_2 = filtered_trans_2.filter(source_id__in=dest_places.values('district_id'))
        
        # If we get 0 transporters from last filter, we'll have to convert the result to queryset
        # to keep consistency. All our filtered_tran will be querysets.
        if filtered_trans_2.count() == 0:
            filtered_trans_2 = TransporterProfile.objects.none()
        
        # Define a local var to store the combined queryset
        filtered_trans = TransporterProfile.objects.none()
        # Union is used to combine querysets. We could have used | operator but it is producing
        # errors.
        filtered_trans = filtered_trans_1.union(filtered_trans_2)
        
        # Last step, we filter for load_type and vehicle_type.
        filtered_trans = filtered_trans.filter(load_type__exact=load_type, \
            vehicle_type_id__in=vehicle_type)

        # Store the transporters list as an array in filtered_trans_list
        filtered_trans_list = filtered_trans.values_list('transporter_id', flat=True).distinct()
        # Get Transporter Queryset from filtered_trans_list
        filtered_trans_qs = Transporter.objects.filter(transporter_id__in=filtered_trans_list)
        # Serializer the qs
        filtered_trans = TransporterSerializer(filtered_trans_qs, many=True)
        # Return the serialized qs
        return filtered_trans


# class MatchingTransOld(generics.ListAPIView):
#     """
#     Search for mathching transporters for a given enquiry.
#     """
#     def get(self, request, *args, **kwargs):
#         enquiry_id = request.query_params.get('enquiry_id')
#         print('Enquiry id is ', enquiry_id)
#         enquiry = Enquiry.objects.get(enquiry_id__exact=enquiry_id)
#         load_type = enquiry.load_type_new
#         vehicle_type = enquiry.vehicle_type.all()
#         print('Load Type: ',load_type)
#         print('Vehicle Type: ',vehicle_type)
#         src_places = enquiry.places.filter(src_dest__exact=Places.Source).\
#             order_by('place_id')
#         dest_places = enquiry.places.filter(src_dest__exact=Places.Destination).\
#             order_by('place_id')
#         src_districts = src_places.values_list('district_id', flat=True)
#         dest_districts = dest_places.values_list('district_id', flat=True)
#         # print(places.district_id_set.all())
#         # src_districts = []
#         # dest_districts = []
#         # for place in src_places:
#         #     src_districts.append(place.district_id)
#         print('Source Districts ',src_districts)
#         print('Destination Districts ',dest_districts)
#         filtered_trans_1 = TransporterProfile.objects.filter(source_id__in=src_districts)
#         filtered_trans_1 = filtered_trans_1.filter(destination_id__in=dest_districts)
#         for trans in filtered_trans_1:
#             print('Filtered Trans 1',trans.transporter_id)
#         if filtered_trans_1.count() == 0:
#             filtered_trans_1 = TransporterProfile.objects.none()
#         print('Places', src_places, dest_places)
#         filtered_trans_2 = TransporterProfile.objects.filter(destination_id__in=src_districts)
#         filtered_trans_2 = filtered_trans_2.filter(source_id__in=dest_districts)
#         if filtered_trans_2.count() == 0:
#             filtered_trans_2 = TransporterProfile.objects.none()
#         for trans in filtered_trans_2:
#             print('Filtered Trans 2',trans.transporter_id)
#         print('Filtered Trans 1: ', filtered_trans_1, 'Filtered Trans 2: ', filtered_trans_2)
#         filtered_trans = TransporterProfile.objects.none()
#         # filtered_trans = filtered_trans_1 | filtered_trans_2
#         # filtered_trans = chain(filtered_trans_1, filtered_trans_2)
#         filtered_trans = filtered_trans_1.union(filtered_trans_2)
#         print('Filtered Trans: ',filtered_trans)
#         filtered_trans = filtered_trans.filter(load_type__exact=load_type, \
#             vehicle_type_id__in=vehicle_type)
#         filtered_trans_list = filtered_trans.values_list('transporter_id', flat=True).distinct()
#         # qs = TransporterProfile.objects.all()
#         # test = qs.values_list('transporter_id', flat=True)
#         # print('Test: ', test)
#         print('filtered_trans_list: ', filtered_trans_list)
#         for trans in filtered_trans:
#             print(trans.transporter_id.transporter_id)
#         return Response(None, status.HTTP_200_OK)
