#!/usr/bin/env python
""" copied from Mezzanine 1.4.16 manage.py """
import os
import sys

# Corrects some pathing issues in various contexts, such as cron jobs,
# and the project layout still being in Django 1.3 format.
from settings import PROJECT_ROOT, PROJECT_DIRNAME, PROJECT_PATH
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(1, PROJECT_PATH)
# Run Django.
if __name__ == "__main__":
    settings_module = "%s.settings" % PROJECT_DIRNAME
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)



