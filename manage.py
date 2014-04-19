#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get('DEV_MODE'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muer.settings_dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muer.settings_production")

    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muer.settings_stage")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
