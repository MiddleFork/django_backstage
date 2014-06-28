"""local wsgi.py file for this Backstage Venue instance.
Contents determined explicitly from this file's location.
"""
import os
import sys

path, name = os.path.split(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % (name))
from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()
