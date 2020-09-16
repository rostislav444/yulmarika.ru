from django.apps import AppConfig


class FilecodesConfig(AppConfig):
    name = 'apps.filecodes'
    verbose_name = "Front Files"

    def ready(self):
       from .models import FileCodes

       filecode = FileCodes.objects.first()
       if not filecode:
           filecode = FileCodes()
           filecode.save()