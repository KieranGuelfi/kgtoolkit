from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def blogview(request):
    return render(request, 'blog.html')
