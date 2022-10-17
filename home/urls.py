from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.homeview, name='homeview'),
    path('ppxl/', include('ppxl.urls')),
    path('blog/', include('blog.urls')),
    path('login/', views.LoginInterfaceView.as_view(), name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout')
]
