import os

"""HARD-CODE the absolute sqlite path and file name
the file is located in the 'db' subfolder of the venue directory
and is named django_backstage.sq3.
"""
f = os.path.abspath(__file__)
settings_dir = os.path.dirname(f)
venue_dir = os.path.dirname(settings_dir)

DBENGINE = 'django.db.backends.sqlite3'
DBHOST = '127.0.0.1'
DBPORT = ''
DBUSER = 'backstage'
DBPASS = ''
DBNAME = os.path.join(venue_dir, 'db/django_backstage.sq3')

DATABASES = {}
DATABASES['default'] = {
    'NAME': DBNAME,
    'ENGINE': DBENGINE,
    'HOST': DBHOST,
    'PORT': DBPORT,
    'USER': DBUSER,
    'PASSWORD': DBPASS
}

DEFAULT_DB_ALIAS='default'
DEFAULT_DB = DATABASES['default']
