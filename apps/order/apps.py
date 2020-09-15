from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'apps.order'
    verbose_name = "Заказы"

    def ready(self):
        from yandex_checkout import Configuration

        try:
            from apps.filecodes.models import YandexKassaAPI
            api = YandexKassaAPI.objects.first()
            Configuration.account_id = api.kassa_num
            Configuration.secret_key = api.kassa_key
        except:
            Configuration.account_id = 740433
            Configuration.secret_key = 'test_vElK711q4bXJlKZJ1W4qTpRzwM5c8Ykwhvc6WzmbZjA'
   