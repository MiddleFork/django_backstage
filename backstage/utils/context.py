from django.http import Http404,HttpResponse
from django.template import loader, Context, RequestContext
from django.shortcuts import render_to_response as r2r


def get_context(request, obj):
    context = RequestContext(request, {'obj': obj, })
    instance = RequestContext(request)
    return context, instance


def render_context(request, obj, template):
    if repr(obj).split(' ')[1] == 'NullObj':
        raise Http404
    try:
        context = RequestContext(request, {'obj': obj, })
        instance = RequestContext(request)
        return r2r(template, context, context_instance=instance)
    except:
        raise


        


