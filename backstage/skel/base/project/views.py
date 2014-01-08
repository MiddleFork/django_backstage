from django.http import HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect,Http404
from django.db import models
from django.shortcuts import render_to_response,redirect
from django.template import loader, Context, RequestContext


def index(request,**kwargs):
    return render_to_response('index.html')
