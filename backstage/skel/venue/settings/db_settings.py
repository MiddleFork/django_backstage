import os

"""HARD-CODE the absolute sqlite path and file name
the file is located in the 'db' subfolder of the venue directory
and is named django_backstage.sq3.
"""
f = os.path.abspath(__file__)
settings_dir = os.path.dirname(f)
venue_dir, settings_name = os.path.split(settings_dir)
venue_parent, venue_name = os.path.split(venue_dir)

DBENGINE = 'django.db.backends.postgresql_psycopg2'
DBHOST = '127.0.0.1'
DBPORT = '5432'
DBUSER = 'backstage'
DBPASS = ''
DBNAME = 'backstage_%s' % venue_name

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
