""" venue-specific settings """
import os
from common_settings import VENUE_ROOT
from db_settings import DATABASES
DEBUG = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(VENUE_ROOT, 'cstatic')) #Collected Static

#APPS specifict to this venue which should be appended to INSTALLED_APPS
VENUE_APPS = []