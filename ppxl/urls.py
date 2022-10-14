from django.urls import path

from . import views

urlpatterns = [
    path('ppxl/', views.upload_file, name='upload_file'),
    path('mptp/', views.mptpedit, name='mptpedit')
]
