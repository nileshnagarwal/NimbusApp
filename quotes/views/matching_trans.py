"""
Search suitable Transporters based on enquiry
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from quotes.models import Enquiry
from masters.models import Places, TransporterProfile, Transporter

# Create your views here
class MatchingTrans(generics.ListAPIView):
    """
    Search for mathching transporters for a given enquiry.
    """
    def get(self, request, *args, **kwargs):        
        enquiry_id = request.query_params.get('enquiry_id')
        print('Enquiry id is ', enquiry_id)
        enquiry = Enquiry.objects.get(enquiry_id__exact=enquiry_id)
        load_type = enquiry.load_type_new
        vehicle_type = enquiry.vehicle_type.all()
        print('Load Type: ',load_type)
        print('Vehicle Type: ',vehicle_type)
        src_places = enquiry.places.filter(src_dest__exact=Places.Source).\
            order_by('place_id')
        dest_places = enquiry.places.filter(src_dest__exact=Places.Destination).\
            order_by('place_id')
        src_districts = src_places.values_list('district_id', flat=True)
        dest_districts = dest_places.values_list('district_id', flat=True)
        # print(places.district_id_set.all())
        # src_districts = []
        # dest_districts = []
        # for place in src_places:
        #     src_districts.append(place.district_id)
        print('Source Districts ',src_districts)
        print('Destination Districts ',dest_districts)
        filtered_trans_1 = TransporterProfile.objects.filter(source_id__in=src_districts)
        filtered_trans_1 = filtered_trans_1.filter(destination_id__in=dest_districts)
        for trans in filtered_trans_1:
            print('Filtered Trans 1',trans.transporter_id)
        if filtered_trans_1.count() == 0:
            filtered_trans_1 = TransporterProfile.objects.none()
        print('Places', src_places, dest_places)
        filtered_trans_2 = TransporterProfile.objects.filter(destination_id__in=src_districts)
        filtered_trans_2 = filtered_trans_2.filter(source_id__in=dest_districts)
        if filtered_trans_2.count() == 0:
            filtered_trans_2 = TransporterProfile.objects.none()
        for trans in filtered_trans_2:
            print('Filtered Trans 2',trans.transporter_id)
        print(filtered_trans_1, filtered_trans_2)
        filtered_trans = TransporterProfile.objects.none()
        filtered_trans = filtered_trans_1 | filtered_trans_2
        print(filtered_trans)
        filtered_trans = filtered_trans.filter(load_type__exact=load_type, \
            vehicle_type_id__in=vehicle_type)
        filtered_trans_list = filtered_trans.values_list('transporter_id', flat=True)
        for trans in filtered_trans_list:
            print(Transporter.objects.get(transporter_id=trans))
        return Response(None, status.HTTP_200_OK)
