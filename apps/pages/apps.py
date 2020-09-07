from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'apps.pages'
    verbose_name = 'Страницы магазина "О нас", "Контакты", "Доставка"'

    def ready(self):
        from .models import generate_pages
        generate_pages()

        
        