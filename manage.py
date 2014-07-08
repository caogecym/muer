#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get('APP_MODE') == 'DEV':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muer.settings_dev")
    elif os.environ.get('APP_MODE') == 'STAGE':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muer.settings_stage")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muer.settings_production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
