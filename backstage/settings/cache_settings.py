#!/usr/bin/python
#cache_settings.py
CACHES = True
#CACHES=False

if CACHES:
    CACHES = dict(default={
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 7200, #ONE HOUR = 7200SEC
        'OPTIONS': {
        }
    }, dummy={
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    })
    #cache settings
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = '7200' #2HR
    CACHE_MIDDLEWARE_KEY_PREFIX = ''

else:
    CACHES = {}

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

DEFAULT_CACHE_ALIAS = 'default'
