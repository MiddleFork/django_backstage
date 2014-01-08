#!/usr/bin/python
import os,sys

PROJECT_DB = 'enterprise'

SITE_ID=1
ADMINS = ()
MANAGERS = ADMINS
USE_TZ = False
TIME_ZONE = None
#TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
SECRET_KEY = '0p3ffc)q#f-4rv23&amp;yqp-f_p04p(lp(i!&amp;wljvvnk690=!0wo$'

EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

INTERNAL_IPS=('127.0.0.1',)

#location of templates
PROJECT_TEMPLATE_DIRS = ['project/templates',]


#context processors
PROJECT_TEMPLATE_CONTEXT_PROCESSORS = [
    'backstage.utils.context_processors.settings_constants',
]

#automatically convert spaces to underscores
UNDERSCORIFY=True
