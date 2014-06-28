#!/usr/bin/env python
""" copied from Mezzanine 1.4.16 manage.py """
import os
import sys

# Corrects some pathing issues in various contexts, such as cron jobs,
# and the venue layout still being in Django 1.3 format.
from settings import VENUE_ROOT, VENUE_DIRNAME, VENUE_PATH
os.chdir(VENUE_ROOT)
sys.path.insert(0, VENUE_ROOT)
sys.path.insert(1, VENUE_PATH)
# Run Django.
if __name__ == "__main__":
    settings_module = "settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)



