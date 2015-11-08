#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # add our project to the path
    sys.path.insert(0, os.path.join("../", ""))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests_project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
