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
    LorryReceiptSerializer, ItemSerializer, LorryVerifySerializer


class LorryReceiptNoList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LorryReceiptNo.objects.all().order_by('lr_no')
    serializer_class = LorryReceiptNoSerializer
    pagination_class = None

    # Overriding post method to generate verification code
    def post(self, request, *args, **kwargs):
        # Generate the verification code and check for uniqueness
        while True:
            verification_no = id_generator()
            if (LorryReceiptNo.objects.filter(verification_no__exact=verification_no)\
                .count() == 0):
                break
        # Modify request data to store verification_no and user_id
        data_copy = request.data.copy()
        data_copy['verification_no'] = verification_no
        data_copy['user_id'] = request.user.id
        serializer = LorryReceiptNoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # Get only the LR Nos for which LR has not been generated yet
        lr_nos = LorryReceiptNo.objects.filter(lr_details__isnull=True)
        serializer = LorryReceiptNoSerializer(lr_nos, many=True)
        if len(serializer.data)>0:
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(None, status.HTTP_204_NO_CONTENT)
        
class LorryReceiptNoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LorryReceiptNo.objects.all().order_by('lr_no')
    serializer_class = LorryReceiptNoSerializer
  
class LorryReceiptList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LorryReceipt.objects.all().order_by('lr_no_id')
    serializer_class = LorryReceiptSerializer
    pagination_class = None

    def post(self, request, *args, **kwargs):
        """
        Overriding the post method
        """
        # Get item list seperated from request data
        try:
            data_copy = request.data.copy()
            data_copy['user_id'] = request.user.id
            items = request.data.get("items")
            # If items datatype is str, convert to list
            if(type(items)==str):
                items = json.loads(items)
        except (ObjectDoesNotExist, KeyError):
            # If items not provided, return error
            return Response("Item list not provided", status.HTTP_400_BAD_REQUEST)
        lr_ser = LorryReceiptSerializer(data=data_copy)
        if not lr_ser.is_valid():
            return Response(lr_ser.errors, status.HTTP_400_BAD_REQUEST)
        else:
            lr = lr_ser.save()
            # Add lr_no to items
            try:
                for item in items:
                    item['lr_no_id'] = lr.lr_no_id.lr_no
                # Save items and check validity
                items_ser = ItemSerializer(data=items, many=True)
                if not items_ser.is_valid():
                    # If error occurs while saving items raise error and delete lr
                    lr.delete()
                    return Response(items_ser.errors, status.HTTP_400_BAD_REQUEST)
                else:
                    items_ser.save()
                    return Response(lr_ser.data, status.HTTP_201_CREATED)
            # If error occurs while saving items raise error and delete lr
            except:
                lr.delete()
                return Response("Unknown Error Occured while saving items", \
                    status.HTTP_500_INTERNAL_SERVER_ERROR)

class LorryReceiptVerify(generics.CreateAPIView):
    """
    Check if the LR No and verification code combination matched with our
    database and return the LR detailed page if matches.
    """
    queryset = LorryReceipt.objects.all().order_by('lr_no_id')
    serializer_class = LorryVerifySerializer
    
    def post(self, request, *args, **kwargs):
        # Get LR No and verification code from request
        try:
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
            return Response("The verification and lr_no combination does not " \
                "match", status.HTTP_400_BAD_REQUEST)
        # Match the verification no received with the verification no saved
        # in our database
        if (verification_no==lr.verification_no):
            # Check if LR has been generated for the given LR No
            try:
                lr_details = LorryReceipt.objects.get(pk=lr_no)
            except (ObjectDoesNotExist, KeyError):
                return Response("LR No is generated but LR details not filled yet.",\
                    status.HTTP_200_OK)            
            lr_ser = LorryVerifySerializer(instance=lr_details)
            return Response(lr_ser.data, status.HTTP_200_OK)
        else:
            return Response("The verification and lr_no combination does not " \
                "match", status.HTTP_400_BAD_REQUEST)

class LorryReceiptNoUniqueCheck(generics.CreateAPIView):
    """
    Check if the given LR No is unique
    """
    permission_classes = (IsAuthenticated, )
    queryset = LorryReceiptNo.objects.all().order_by('lr_no')
    serializer_class = LorryReceiptNoSerializer

    def post(self, request, *arg, **kwargs):
        data_copy = request.data.copy()
        lr_no = data_copy.get('lr_no', None)
        """
        If JSON data is sent to api then we get Dict datatype in request.data.
        Else if form-data is sent to api we get QueryDict datatype.
        For QueryDict we need to convert the lr_no from str to int. 
        In case of Dict the lr_no will already be int so this step will be 
        skipped.
        """
        if (type(lr_no) is str):
            try:
                lr_no = int(lr_no)
            except ValueError:
                return Response("LR No needs to be an integer", \
                    status.HTTP_400_BAD_REQUEST)
        if (lr_no is None or lr_no is ''):
            return Response("LR No needs to be provided", \
                status.HTTP_400_BAD_REQUEST)
        if (LorryReceiptNo.objects.filter(pk=lr_no).count()==0):
            return Response(True,status.HTTP_200_OK)
        else:
            return Response(False, status.HTTP_200_OK)

class OldestEmptyLorryReceiptNo(generics.ListAPIView):
    """
    Retrieve the oldest LR No that has not yet been engaged
    """
    permission_classes = (IsAuthenticated, )
    queryset = LorryReceiptNo.objects.all().order_by('lr_no')
    serializer_class = LorryReceiptNoSerializer

    def get(self, request, *args, **kwargs):
        # Get lr_no if provided
        data_copy = request.data.copy()        
        lr_no = data_copy.get('lr_no', None)
        """
        If JSON data is sent to api then we get Dict datatype in request.data.
        Else if form-data is sent to api we get QueryDict datatype.
        For QueryDict we need to convert the lr_no from str to int. 
        In case of Dict the lr_no will already be int so this step will be 
        skipped.
        """
        if (type(lr_no) is str):
            try:
                lr_no = int(lr_no)
            # if lr_no is not int, return error
            except ValueError:
                return Response("LR No needs to be an integer", \
                status.HTTP_400_BAD_REQUEST)
        # If lr_no is not provided, consider it to be 1
        if (lr_no is None or lr_no==0):
            lr_no = 1        
        # Search for empty lr_no
        lr_no = empty_lr_search(lr_no)
        return Response(lr_no, status.HTTP_200_OK)
        

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

def lr_unique_check(lr_no):
    if (LorryReceiptNo.objects.filter(pk=lr_no).count()==0):
        return True
    else:
        return False

def empty_lr_search(lr_no=1):
    """
    Find the oldest LR no which has not been engaged yet.
    We take the starting lr_no as argument to begin searching from.
    """
    
    not_found = True
    while not_found:
        if (LorryReceiptNo.objects.filter(pk=lr_no).count() == 0):
            not_found = False
            return lr_no
        else:
            lr_no += 1
