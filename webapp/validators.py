from rest_framework import serializers
from django.utils.deconstruct import deconstructible
import re

# @deconstructible decorator is used to let django serialize 
# this class. Without this makemigrations throws an error.
# Refer: https://docs.djangoproject.com/en/1.11/topics/ (cont)
# migrations/#adding-a-deconstruct-method
@deconstructible
class MobileValidation(object):
    """ This custom validator checks if the given value
    contains only digits, has the specified exact 'length'
    and starts with the specified 'start_with' digits."""

    def __init__(self, length, start_with):
        self.length = length
        self.start_with = start_with

    def __call__(self, value):
        if re.match('^[' + self.start_with + '][0-9]{' + str(self.length-1) + '}$', value):
            pass
        else:
            message = 'The mobile number should exactly be of %d digits, starting with %s' \
                %(self.length, self.start_with) + ' not containing any chars/space' 
            raise serializers.ValidationError(message)