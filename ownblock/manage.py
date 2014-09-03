#!/usr/bin/env python
import os
import sys
import dotenv

dotenv.read_dotenv()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ownblock.settings")

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
