from django import template
from django.conf import settings

register = template.Library()

# settings value
@register.simple_tag
def csettings(name):
    """ provides for the inclusion of setting variables within a template. """
    return getattr(settings, name, "")
