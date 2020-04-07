"""
URL for the Operations Module.
"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^operations/lr_no/$', views.LorryReceiptNoList.as_view()),
    url(r'^operations/lr_no/(?P<pk>[0-9]+)/$', views.LorryReceiptNoDetail.as_view()),
    url(r'^operations/lr/$', views.LorryReceiptList.as_view()),
    url(r'^operations/lr/(?P<pk>[0-9]+)/$', views.LorryReceiptDetail.as_view()),
    url(r'^operations/item/$', views.ItemList.as_view()),
    url(r'^operations/item/(?P<pk>[0-9]+)/$', views.ItemDetail.as_view()),
    url(r'^operations/lr_verify/$', views.LorryReceiptVerify.as_view()),
    url(r'^operations/lr_unique_check/$', views.LorryReceiptNoUniqueCheck.as_view()),
    url(r'^operations/lr_search_empty/$', views.OldestEmptyLorryReceiptNo.as_view()),
]
