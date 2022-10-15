from django.urls import path

from . import views
from .views import MPTPList

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('mptplist/', MPTPList.as_view(), name='mptplist')
]
