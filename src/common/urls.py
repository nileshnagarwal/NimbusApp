"""
URL for the Common Module.
"""
from django.conf.urls import url
from .views import UserList, UserDetail
from . import views

urlpatterns = [
    url(r'^common/user/$', views.UserList.as_view()),
    url(r'^common/user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]