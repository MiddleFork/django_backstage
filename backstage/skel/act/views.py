from django.shortcuts import HttpResponse
from django.views.generic import View

def index(request):
    return HttpResponse('hello world')

