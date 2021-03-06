#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TravelPlanner.settings")

    import TravelPlanner.startuputil as startup
    startup.loadtraindata()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
