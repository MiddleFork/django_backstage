from django import template
register = template.Library()

@register.filter
def underscore(string):
    if string is not None:
        return string.replace(' ','_')
    else:
        return ''
