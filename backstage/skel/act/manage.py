#!/usr/bin/env python
import os
import sys

# Run Django.
if __name__ == "__main__":
    settings_module = "settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)



