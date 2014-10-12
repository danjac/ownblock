from django.apps import AppConfig


from .models import connect_signals


class AccountsAppConfig(AppConfig):
    name = "ownblock.apps.accounts"

    def ready(self):

        connect_signals()
