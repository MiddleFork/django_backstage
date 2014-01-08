""" local.settings
This is where you set your own localizations
for a specific instance of a Backstage project.

Any valid django settings which are set here will
over-ride Backstage and Django defaults.  Any other variables you set here
will also be set in your project's Settings namespace as well

#
*Some* of the Settings you'll most likely wish to set here include
DATABASES
STATIC_URL
MEDIA_URL
DEBUG
TEMPLATE_DEBUG

You can modify without replacing any list-type setting (INSTALLED_APPS, TEMPLATE_DIRS, etc) by
using the proper list.insert(0,'blah') or list.append('blah') syntax as in
INSTALLED_APPS.append('my.awesome.app')
"""
from local_settings import *
