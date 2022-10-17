from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.


def homeview(request):
    return render(request, 'home/home.html')


class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'


class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'
