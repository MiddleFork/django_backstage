"""
settings_tags.py
This file provides a simple Django Templatetag
to expose the app's settings values in the HTML 
template environment. Settings are stored as 'csettings'
to avoid a name conflict 
and accesses as {{ csettings.FOO }} in the templates.
""" 

from django import template
from django.conf import settings

register = template.Library()

# settings value
@register.simple_tag
def csettings(name):
    """ provides for the inclusion of setting variables within a template. """
    return getattr(settings, name, "")
