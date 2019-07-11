from django.apps import AppConfig


class ScribeaccountConfig(AppConfig):
    name = 'ScribeAccount'

    def ready(self):
        import ScribeAccount.signals
