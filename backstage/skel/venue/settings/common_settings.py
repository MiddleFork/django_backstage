#!/usr/bin/python
"""This is the overall settings module for a single Backstage Venue instance
 It will import settings from the Backstage package, and may over-ride them.
 In turn, each Backstage Act instance will import these settings, and may over-ride them."""
#
#
#### DO NOT EDIT THIS FILE ####
#
#
import os
import sys

#Assume that 'manage.py' and 'settings.py' are siblings at the root of the Backstage venue instance
#Also assume this file is in a directory named 'settings' (as called by __init__.py) and thus
#we the venue root is at the parent level.
SETTINGS_PATH = os.path.dirname(os.path.abspath(__file__))
VENUE_ROOT = os.path.dirname(SETTINGS_PATH)
VENUE_PATH, VENUE_DIRNAME = os.path.split(VENUE_ROOT)
VENUE_NAME = VENUE_DIRNAME
ROOT_URLCONF = "%s.urls" % VENUE_NAME

VENUE_PATH in sys.path or sys.path.append(VENUE_PATH)

"""
Here, we import all the Backstage default settings,
which in turn imports all of Django's default settings, etc...
"""
from backstage.settings.backstage_settings import *

###Here, we extend and over-ride them....

#Extend INSTALLED_APPS
INSTALLED_APPS = list(INSTALLED_APPS) #cast as alist to avoid tuple issues.
VENUE_NAME in INSTALLED_APPS or INSTALLED_APPS.insert(0, VENUE_NAME)
#venue_app = '%s.venue' % VENUE_PATH
#venue_app in INSTALLED_APPS or INSTALLED_APPS.insert(1, venue_app)

INSTALLED_APPS.append('django.contrib.gis')
s = "INSTALLED_APPS.append('%s.instruments.local')" % VENUE_NAME
exec(s)
del(s)
