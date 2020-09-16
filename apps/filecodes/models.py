from django.db import models
from project.settings import MEDIA_ROOT
import os


class FileField(models.FileField):
    def save_form_data(self, instance, data):
        file = getattr(instance, self.attname)
        if file != data:
            try: os.remove(file.path)
            except: pass
        super(FileField, self).save_form_data(instance, data)


class FileCodes(models.Model):
    meta_title = models.CharField(max_length=300, blank=True, null=True, verbose_name="Мета тег Titile (Домашней страницы)")
    meta_descr = models.TextField(max_length=500, blank=True, null=True, verbose_name="Мета тег Description (Домашней страницы)")

    logo =      FileField(upload_to="file_codes", blank=True, null=True, verbose_name="Логотип сайта")
    favicon =   FileField(upload_to="file_codes", blank=True, null=True, verbose_name="Fav icon")
    css =       FileField(upload_to="file_codes", blank=True, null=True,  verbose_name="Файлы стилей")
    free_delivery = models.PositiveIntegerField(default=1000, blank=True,  verbose_name="Бесплатная доставка от")
    base_delivery = models.PositiveIntegerField(default=400, blank=True,  verbose_name="Базовая стоимость доставки")

    minimal_order = models.PositiveIntegerField(default=500,  blank=True,  verbose_name="Минимальная сумма заказа")
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

class TelegramAPI(models.Model):
    chanel_id =  models.CharField(
        max_length=500, 
        default="1270278191", 
        blank=True, null=True, 
        verbose_name="ID канала", 
        help_text="Его можно взять из URL в браузерной версии Telegram между 'c' и '_'"
    )
    api_key =    models.CharField(
        max_length=500, 
        default="1130353501:AAHQWTGljZtT39hv5cohgQ8scmp42BFp7GU", 
        blank=True, null=True, 
        verbose_name="API ключ", 
        help_text="Дается а чате BotFather при создании бота, которго потому нужно назначить администратором канала"
    )

    class Meta:
        verbose_name = "API Telegram"
        verbose_name_plural = "API Telegram"

class YandexKassaAPI(models.Model):
    kassa_num = models.CharField(max_length=500, blank=True, null=True, verbose_name="ID аккаунта")
    kassa_key = models.CharField(max_length=500, blank=True, null=True, verbose_name="Секретный ключ")

    class Meta:
        verbose_name = "API Яндекс Кассы"
        verbose_name_plural = "API Яндекс Кассы"


class YandexMailAPI(models.Model):
    email    = models.EmailField(max_length=500, default="yulmarika@yandex.ru", blank=False,  verbose_name="Email")
    password = models.CharField(max_length=500,  default="Cr3-XK5-db8-CRf",     blank=False,  verbose_name="Пароль от почты")
    smtp =     models.CharField(max_length=500,  default="smtp.yandex.com",     blank=False,  verbose_name="SMTP") 

    class Meta:
        verbose_name = "API Яндекс Почты"
        verbose_name_plural = "API Яндекс Почты"