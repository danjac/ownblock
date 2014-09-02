#!/usr/bin/env python
import os
import dotenv

dotenv.read_dotenv()

if __name__ == "__main__":

    os.environ['DJANGO_SETTINGS_MODULE'] = 'ownblock.settings.test'

    from django.core.management import call_command

    call_command("test")
