from django import forms
from django.contrib import admin
from django.db import models

from .models import LorryReceipt, LorryReceiptNo, Item

# Register your models here.

admin.site.register(LorryReceiptNo)
admin.site.register(LorryReceipt)
admin.site.register(Item)
