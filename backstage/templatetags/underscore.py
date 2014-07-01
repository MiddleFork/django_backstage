"""
A simple TemplateTag to provide
in-template on-the-fly string underscoring
Usage:  {{ some%20string | underscore }} becomes some_string
"""

from django import template
register = template.Library()

@register.filter
def underscore(string):
    if string is not None:
        return string.replace(' ','_')
    else:
        return ''
