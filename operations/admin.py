from django.contrib import admin

from .models import LorryReceipt, LorryReceiptNo, Item

# Register your models here.

admin.site.register(LorryReceiptNo)
admin.site.register(LorryReceipt)
admin.site.register(Item)
