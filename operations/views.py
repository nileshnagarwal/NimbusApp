"""Views for Operations Module"""

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

import string
import random
import json

from .models import LorryReceipt, LorryReceiptNo, Item
from .serializers import LorryReceiptNoSerializer, \
    LorryReceiptSerializer, ItemSerializer


class LorryReceiptNoList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LorryReceiptNo.objects.all().order_by('lr_no')
    serializer_class = LorryReceiptNoSerializer

    # Overriding post method to generate verification code
    def post(self, request, *args, **kwargs):
        # Generate the verification code and check for uniqueness
        while True:
            verification_no = id_generator()
            if (LorryReceiptNo.objects.filter(verification_no__exact=verification_no)\
                .count() == 0):
                break
        # Modify request data to store verification_no
        data_copy = request.data.copy()
        data_copy['verification_no'] = verification_no
        serializer = LorryReceiptNoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages, status.HTTP_400_BAD_REQUEST)

class LorryReceiptNoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LorryReceiptNo.objects.all().order_by('lr_no')
    serializer_class = LorryReceiptNoSerializer
  
class LorryReceiptList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LorryReceipt.objects.all().order_by('lr_no_id')
    serializer_class = LorryReceiptSerializer

    def post(self, request, *args, **kwargs):
        """
        Overriding the post method
        """
        # Get item list seperated from request data
        try:
            data_copy = request.data.copy
            items = request.data.get("items")
            items = json.loads(items)
        except (ObjectDoesNotExist, KeyError):
            return Response("Item list not provided", status.HTTP_400_BAD_REQUEST)
        lr_ser = LorryReceiptSerializer(data=request.data)
        if not lr_ser.is_valid():
            return Response(lr_ser.error_messages, status.HTTP_400_BAD_REQUEST)
        else:
            lr = lr_ser.save()
            # Add lr_no to items
            try:
                for item in items:
                    item['lr_no_id'] = lr.lr_no_id.lr_no
                # Save items and check validity
                items_ser = ItemSerializer(data=items, many=True)
                if not items_ser.is_valid():
                    return Response(items_ser.error_messages, status.HTTP_400_BAD_REQUEST)
                else:
                    items_ser.save()
                    return Response(lr_ser.data, status.HTTP_201_CREATED)
            # If error occurs while saving items raise error and delete lr
            except:
                LorryReceipt.objects.get(pk=lr.lr_no_id).delete()
                return Response("Unknown Error Occured while saving items", \
                    status.HTTP_500_INTERNAL_SERVER_ERROR)

class LorryReceiptVerify(generics.ListAPIView):
    """
    Check if the LR No and verification code combination matched with our
    database and return the LR detailed page if matches.
    """
    permission_classes = (IsAuthenticated,)
    queryset = LorryReceipt.objects.all().order_by('lr_no_id')
    serializer_class = LorryReceiptSerializer
    
    def post(self, request, *args, **kwargs):
        # Get LR No and verification code from request
        try:
            print(request.data)
            lr_no = request.data.get('lr_no', None)
            verification_no = request.data.get('verification_no', None)
            if (lr_no is None or verification_no is None):
                raise ObjectDoesNotExist
        except (ObjectDoesNotExist, KeyError):
            return Response("LR No and Verification No to be provided for "\
                "verification", status.HTTP_400_BAD_REQUEST)
        # Retrieve the LR from db using the lr_no received
        try:
            lr = LorryReceiptNo.objects.get(pk=lr_no)
        except (ObjectDoesNotExist, KeyError):
            return Response("No LR has been allocated with the given LR No")
        # Match the verification no received with the verification no saved
        # in our database
        if (verification_no==lr.verification_no):
            # Check if LR has been generated for the given LR No
            try:
                lr_details = LorryReceipt.objects.get(pk=lr_no)
            except (ObjectDoesNotExist, KeyError):
                return Response("LR No is generated but LR details not filled yet.",\
                    status.HTTP_200_OK)            
            lr_ser = LorryReceiptSerializer(instance=lr_details)
            return Response(lr_ser.data, status.HTTP_200_OK)
        else:
            return Response("The verification and lr_no combination does not " \
                "match", status.HTTP_400_BAD_REQUEST)

class LorryReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LorryReceipt.objects.all().order_by('lr_no_id')
    serializer_class = LorryReceiptSerializer

class ItemList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all().order_by('item_id')
    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all().order_by('item_id')
    serializer_class = ItemSerializer

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
