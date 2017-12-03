from django.conf.urls import url
from masters import views

urlpatterns = [
    url(r'^masters/vehicletype/$', views.Vehicle_TypeList.as_view()),
    url(r'^masters/vehiclebody/$', views.Vehicle_BodyList.as_view()),
    url(r'^masters/vehicletype/(?P<pk>[0-9]+)/$', views.Vehicle_TypeDetail.as_view()),
    url(r'^masters/vehiclebody/(?P<pk>[0-9]+)/$', views.Vehicle_BodyDetail.as_view()),
    url(r'^masters/transporter/$', views.TransporterList.as_view()),
    url(r'^masters/transporter/(?P<pk>[0-9]+)/$', views.TransporterDetail.as_view()),
]
