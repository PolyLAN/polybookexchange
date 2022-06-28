from django.apps import AppConfig
from django.contrib.auth import get_user_model


class PolyBookExchangeConfig(AppConfig):

    name = "polybookexchange"

    def ready(self):
        super(PolyBookExchangeConfig, self).ready()

        User = get_user_model()

        if "get_sciper" not in User.__dict__:
            def __get_sciper(self):
                return self.username

            User.get_sciper = __get_sciper
