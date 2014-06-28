#!/usr/bin/python
"""STATIC SETTINGS
settings for static content
These are default somewhat sane values that
almost certainly will not work off-the shelf and
should be modified """

import sys,os
STATIC_ROOT = '/data/www/static/'
STATIC_URL = 'http://127.0.0.1/static/'

#WEBUSER necessesary for uploads??
WEBUSER = 'backstage'

STATICFILES_DIRS = []

#MEDIA_ROOT set within site settings.py
MEDIA_ROOT_BASE = '/data/www/content/site/'
MEDIA_URL = 'http://127.0.0.1/media/'

ADMIN_MEDIA_PREFIX =  STATIC_URL + "grappelli/"
AUTOCOMPLETE_MEDIA_PREFIX='/media/autocomplete'

