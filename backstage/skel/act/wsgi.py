"""local wsgi.py file for this Backstage Act instance.
Contents determined explicitly from this file's location.
"""
import os
import sys

#path name for this Act

acts_path, act_name = os.path.split(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,acts_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % (act_name))
from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()
