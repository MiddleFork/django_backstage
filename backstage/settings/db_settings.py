DBENGINE = 'django.db.backends.sqlite3'
DBHOST = '127.0.0.1'
DBPORT = ''
DBUSER = ''
DBPASS = ''
DBNAME = 'django_backstage.sq3'

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
