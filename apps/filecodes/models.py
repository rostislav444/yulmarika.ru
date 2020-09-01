from django.db import models
import os


class FileField(models.FileField):
    def save_form_data(self, instance, data):
        file = getattr(instance, self.attname)
        if file != data:
            try: os.remove(file.path)
            except: pass
        super(FileField, self).save_form_data(instance, data)


class FileCodes(models.Model):
    logo =      FileField(upload_to="file_codes", verbose_name="Логотип сайта")
    favicon =   FileField(upload_to="file_codes", verbose_name="Fav icon")
    css =       FileField(upload_to="file_codes",  verbose_name="Файлы стилей")
    showcase =  models.PositiveIntegerField(default=12, blank=False,  verbose_name="Колличесвто товаров на витрине")
    recomend =  models.PositiveIntegerField(default=24, blank=False,  verbose_name="Колличесвто товаров в блоке рекомендуем")
    phone =     models.CharField(max_length=255)
    copyright = models.CharField(max_length=255, verbose_name="Текст копирайта футера")
    title =     models.CharField(max_length=255, verbose_name="Заголовок (приветствие)")

    class Meta:
        verbose_name = "Коды и файлы"
        verbose_name_plural = "Коды и файлы"


class SocialIcons(models.Model):
    parent = models.ForeignKey(FileCodes, on_delete=models.CASCADE, related_name="icons")
    name =   models.CharField(max_length=255,  verbose_name='Название блока (всплывающая подсказака)')
    url =    models.CharField(max_length=500,  verbose_name='Ссылка на ресурс')
    icon =   FileField(upload_to='icons', verbose_name='Иконка блока')
    
    class Meta:
        verbose_name = "Данные соц. сетей в футере"
        verbose_name_plural = "Данные соц. сетей в футере"
