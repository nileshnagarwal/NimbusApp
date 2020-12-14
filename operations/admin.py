from django import forms
from django.contrib import admin
from django.db import models

from .models import LorryReceipt, LorryReceiptNo, Item
from ckeditor.widgets import CKEditorWidget

# Register your models here.

class LorryReceiptAdminForm(forms.ModelForm):
    consignor_manual = forms.CharField(widget=CKEditorWidget())
    consignee_manual = forms.CharField(widget=CKEditorWidget())
    comment = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = LorryReceipt
        fields = '__all__'

class LorryReceiptAdmin(admin.ModelAdmin):
    form = LorryReceiptAdminForm

admin.site.register(LorryReceiptNo)
admin.site.register(LorryReceipt, LorryReceiptAdmin)
admin.site.register(Item)
