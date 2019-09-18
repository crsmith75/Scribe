from django.apps import AppConfig


class TwitteraccountsConfig(AppConfig):
    name = 'twitteraccounts'


    def ready(self):
        import twitteraccounts.signals
