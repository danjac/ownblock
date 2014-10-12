from django.apps import AppConfig


from .models import connect_signals


class BuildingsAppConfig(AppConfig):
    name = "ownblock.apps.buildings"

    def ready(self):
        connect_signals()
