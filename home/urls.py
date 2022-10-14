from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.homeview, name='homeview'),
    path('ppxl/', include('ppxl.urls')),
    path('blog/', include('blog.urls')),
]
