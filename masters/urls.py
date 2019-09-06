from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^masters/vehicletype/$', views.VehicleTypeList.as_view()),
    url(r'^masters/vehiclebody/$', views.VehicleBodyList.as_view()),
    url(r'^masters/vehicletype/(?P<pk>[0-9]+)/$', views.VehicleTypeDetail.as_view()),
    url(r'^masters/vehiclebody/(?P<pk>[0-9]+)/$', views.VehicleBodyDetail.as_view()),
    url(r'^masters/transporter/$', views.TransporterList.as_view()),
    url(r'^masters/transporter/(?P<pk>[0-9]+)/$', views.TransporterDetail.as_view()),
    url(r'^masters/extraexpenses/$', views.ExtraExpensesList.as_view()),
    url(r'^masters/extraexpenses/(?P<pk>[0-9]+)/$', views.ExtraExpensesDetail.as_view()),
    url(r'^masters/places/$', views.PlacesList.as_view()),
    url(r'^masters/places/(?P<pk>[0-9]+)/$', views.PlacesDetail.as_view()),
    url(r'^masters/districts/$', views.DistrictList.as_view()),
    url(r'^masters/districts/(?P<pk>[0-9]+)/$', views.DistrictDetail.as_view()),
]
