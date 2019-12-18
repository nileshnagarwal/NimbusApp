"""
Add address and administrative_level_1 and locality to places
"""
from rest_framework import generics
import requests
from rest_framework.response import Response
from rest_framework import status

from masters.models import Places

from webapp.settings import GOOGLE_API_SETTINGS
# Create your views here
class UpdatePlacesLocality(generics.ListAPIView):
    """
    Add address and administrative_level_1 and locality to places
    """
    def get(self, request, *args, **kwargs):
        # Get all places having blank address field
        places = Places.objects.filter(address__isnull=True)
        # URL and key of google maps api
        url = GOOGLE_API_SETTINGS['URL']
        api_key = GOOGLE_API_SETTINGS['API_KEY']
        
        # Loop through all the places to get address from api and save the same
        for place in places:
            location = place.place

            # defining a params dict for the parameters to be sent to the API 
            params = {'address':location, 'key': api_key}

            # sending get request and saving the response as response object 
            r = requests.get(url = url, params = params)
            
            # extracting data in json format 
            data = r.json()

            # Getting address components which is a json object.
            # We will get locality, sub_locality etc from address components
            address_components = data['results'][0]['address_components']

            # Saving the response received in the jsonfield: address
            place.address = data

            # Looping through address_components to search for locality, 
            # sub_locality etc and saving it to the places db
            for address in address_components:
                # if address['types'].index('locality')>=0:
                if 'sublocality_level_1' in address['types']:
                    place.sublocality_level_1 = address['long_name']
                if 'locality' in address['types']:
                    place.locality = address['long_name']
                if 'administrative_area_level_2' in address['types']:
                    place.administrative_area_level_2 = address['long_name']
                if 'administrative_area_level_1' in address['types']:
                    place.administrative_area_level_1 = address['long_name']
            place.save()           

        return Response(None, status.HTTP_200_OK)
