#!/usr/bin/env python
import os
import dotenv
import django
import sys

dotenv.read_dotenv()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_CONFIGURATION", "Test")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ownblock.settings")

    from configurations.management import execute_from_command_line

    django.setup()

    execute_from_command_line([sys.argv[0]] + ["test"] + sys.argv[1:])
