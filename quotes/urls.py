"""
URL for the Quotes Module.
"""

from django.conf.urls import url
from quotes import views

urlpatterns = [
    url(r'^enquiry/$', views.EnquiryList.as_view()),
    url(r'^enquiry/(?P<pk>[0-9]+)/$', views.EnquiryDetail.as_view()),
    url(r'^enquiry_search/$', views.EnquirySearchList.as_view()),
    url(r'^cnf_enquiry/(?P<pk>[0-9]+)/$', views.ConfirmEnquiry.as_view()),
    url(r'^quotes/$', views.SupplierQuoteList.as_view()),
    url(r'^quotes/(?P<pk>[0-9]+)/$', views.SupplierQuoteDetail.as_view()),
    url(r'^quotes/enquiry/(?P<pk>[0-9]+)/$', views.SupplierQuotesForEnquiry.as_view()),
]
