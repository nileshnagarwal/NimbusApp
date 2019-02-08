from django.conf.urls import url
from masters import views

urlpatterns = [
    url(r'^masters/vehicletype/$', views.Vehicle_TypeList.as_view()),
    url(r'^masters/vehiclebody/$', views.Vehicle_BodyList.as_view()),
    url(r'^masters/vehicletype/(?P<pk>[0-9]+)/$', views.Vehicle_TypeDetail.as_view()),
    url(r'^masters/vehiclebody/(?P<pk>[0-9]+)/$', views.Vehicle_BodyDetail.as_view()),
    url(r'^masters/transporter/$', views.TransporterList.as_view()),
    url(r'^masters/transporter/(?P<pk>[0-9]+)/$', views.TransporterDetail.as_view()),
    url(r'^masters/extraexpenses/$', views.Extra_ExpensesList.as_view()),
    url(r'^masters/extraexpenses/(?P<pk>[0-9]+)/$', views.Extra_ExpensesDetail.as_view()),
    url(r'^masters/places/$', views.PlacesList.as_view()),
    url(r'^masters/places/(?P<pk>[0-9]+)/$', views.PlacesDetail.as_view()),
]
