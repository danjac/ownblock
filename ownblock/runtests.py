#!/usr/bin/env python
import os
import dotenv
import django

dotenv.read_dotenv()

if __name__ == "__main__":

    os.environ['DJANGO_SETTINGS_MODULE'] = 'ownblock.settings.test'
    django.setup()

    from django.core.management import call_command

    call_command("test")
