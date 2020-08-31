from django.db import models
from apps.core.models import ModelImages
from django.utils import timezone


# Globals


class Banner(ModelImages):
    name =           models.CharField(max_length=255, verbose_name="Название (Крупный шрифт)")
    description =    models.CharField(max_length=255, verbose_name="Описание (меклий шрифт)", null=True, blank=False)
    url =            models.CharField(max_length=255, verbose_name="Сслыка на страницу", null=True, blank=True)
    image =          models.ImageField(verbose_name="Картинка баннера",  null=True, blank=False)
    image_thmb =     models.TextField(editable=False, null=True, blank=True)
    created =        models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Последнее изменение (сортировка)")

    class Meta:
        ordering = ['-created']
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.name

  