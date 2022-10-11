from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def simpleview(request):
    return HttpResponse('This is a simple view.')
