DBENGINE = 'django.db.backends.postgresql_psycopg2'
DBHOST = '127.0.0.1'
DBPORT = 5433
DBUSER = ''
DBPASS = ''

DATABASES = {}
DATABASES['default'] = {
    'NAME': None,
    'ENGINE': DBENGINE,
    'HOST': DBHOST,
    'PORT': DBPORT,
    'USER': DBUSER,
    'PASSWORD': DBPASS
}

DEFAULT_DB_ALIAS='default'
DEFAULT_DB = DATABASES['default']
