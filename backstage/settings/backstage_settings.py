#!/usr/bin/python
"""Settings File for Django Backstage.  Borrows from Django's own settings.py as well as Mezzanine's settings.py;
Compartmentalizes settings into multiple sub-settings files, including 'database_','cache_','app_','local_'"""
# DJANGO CORE SETTINGS
from backstage.settings.django_settings import *

# SERVER SETTINGS (nginx, uwsgi, etc)
UWSGI_VASSALS = '/etc/uwsgi-emperor/vassals/'
NGINX_BASE = '/etc/nginx/'


# MEZZANINE SETTINGS
try:
    from local.local_settings import Mezzanine
except:
    Mezzanine = True
if Mezzanine:
    from backstage.settings.mezzanine_settings import *

# VENUE SETTINGS (name, path, etc.)
from backstage.settings.venue_settings import *

# DB SETTINGS (default)
from backstage.settings.db_settings import DATABASES

TEMPLATE_DIRS = TEMPLATE_DIRS + venue_TEMPLATE_DIRS
TEMPLATE_CONTEXT_PROCESSORS = venue_TEMPLATE_CONTEXT_PROCESSORS + TEMPLATE_CONTEXT_PROCESSORS

# INSTALLED APPS
from backstage.settings.app_settings import INSTALLED_APPS

# STATIC SETTINGS (media_root, staticfiles, etc)
from backstage.settings.static_settings import *

# IF MEZZAINE IS INSTALLED:
if Mezzanine:
    INSTALLED_APPS = INSTALLED_APPS + MEZZANINE_INSTALLED_APPS

    TEMPLATE_CONTEXT_PROCESSORS = \
        TEMPLATE_CONTEXT_PROCESSORS + MEZZANINE_TEMPLATE_CONTEXT_PROCESSORS
    AUTHENTICATION_BACKENDS = \
        MEZZANINE_AUTHENTICATION_BACKENDS + \
        AUTHENTICATION_BACKENDS
    MIDDLEWARE_CLASSES = MEZZANINE_MIDDLEWARE_CLASSES_PREPEND + \
        MIDDLEWARE_CLASSES + MEZZANINE_MIDDLEWARE_CLASSES_APPEND

    TEMPLATE_DIRS = TEMPLATE_DIRS + MEZZANINE_TEMPLATE_DIRS

    #if mezzanine-flexipage is installed
    try:
        from backstage.settings.flexipage_settings import *
        if FLEXIPAGE:
            INSTALLED_APPS.append('flexipage')
    except:
        pass


# Cache middle ware must bookend all other middleware
# https://docs.djangovenue.com/en/1.4/topics/cache/
if len(CACHES) > 0:
    # this inserts UpdateCache at the beginning
    MIDDLEWARE_CLASSES.insert(0,'django.middleware.cache.UpdateCacheMiddleware')
    # and this appends FetchFromCache at the end
    MIDDLEWARE_CLASSES.append('django.middleware.cache.FetchFromCacheMiddleware')
else:
    pass #CACHES is empty (cache_settings.py)

# misc_settings, didn't know where to put them
from misc_settings import *

# More mezzanine, do at the very end
if Mezzanine:
    try:
        from mezzanine.utils.conf import set_dynamic_settings
    except ImportError:
        pass
    else:
        set_dynamic_settings(globals())







