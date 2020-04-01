from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^masters/vehicletype/$', views.VehicleTypeList.as_view()),
    url(r'^masters/vehicletype/categorywise/$', views.VehicleTypeCategoryWiseList.as_view()),
    url(r'^masters/vehiclebody/$', views.VehicleBodyList.as_view()),
    url(r'^masters/vehicletype/(?P<pk>[0-9]+)/$', views.VehicleTypeDetail.as_view()),
    url(r'^masters/vehiclebody/(?P<pk>[0-9]+)/$', views.VehicleBodyDetail.as_view()),
    url(r'^masters/loadtype/$', views.LoadTypeList.as_view()),
    url(r'^masters/loadtype/(?P<pk>[0-9]+)/$', views.LoadTypeDetail.as_view()),
    url(r'^masters/transporter/$', views.TransporterList.as_view()),
    url(r'^masters/transporter/(?P<pk>[0-9]+)/$', views.TransporterDetail.as_view()),
    url(r'^masters/extraexpenses/$', views.ExtraExpensesList.as_view()),
    url(r'^masters/extraexpenses/(?P<pk>[0-9]+)/$', views.ExtraExpensesDetail.as_view()),
    url(r'^masters/places/$', views.PlacesList.as_view()),
    url(r'^masters/places/(?P<pk>[0-9]+)/$', views.PlacesDetail.as_view()),
    url(r'^masters/districts/$', views.DistrictList.as_view()),
    url(r'^masters/districts/(?P<pk>[0-9]+)/$', views.DistrictDetail.as_view()),
    url(r'^masters/trans_profile/$', views.TransporterProfileList.as_view()),
    url(r'^masters/trans_profile/(?P<pk>[0-9]+)/$', views.TransporterProfileDetail.as_view()),
    url(r'^masters/client/$', views.ClientList.as_view()),
    url(r'^masters/client/(?P<pk>[0-9]+)/$', views.ClientDetail.as_view()),
    url(r'^masters/client_adr/$', views.ClientAddressList.as_view()),
    url(r'^masters/client_adr_by_client_id/$', views.ClientAddressListByClientId.as_view()),
    url(r'^masters/client_adr/(?P<pk>[0-9]+)/$', views.ClientAddressDetail.as_view()),
]
