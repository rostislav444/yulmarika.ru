from django.db import models
from apps.core.models import ModelImages
import os, PIL, io, json, jsonfield
from django.utils.text import slugify
from unidecode import unidecode


class Page(ModelImages):
    name =       models.CharField(max_length=255, verbose_name="Название странциы")
    slug =       models.SlugField(max_length=255, editable=False, null=True, blank=True)
    image =      models.ImageField(verbose_name="Карточка товара (основная)", null=True, blank=True)
    image_thmb = jsonfield.JSONField(editable=False, null=True, blank=True, default='{}')

    class Meta:
        verbose_name = "Страница магазина"
        verbose_name_plural = "Страницы магазина"

    def __str__(self):
        return self.name

    @property
    def make_slug(self):
        return slugify(unidecode('-'.join([self.name])))

    def save(self):
        self.slug = self.make_slug
        super(Page, self).save()


class PageBlock(models.Model):
    parent = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="blocks")
    name = models.CharField(max_length=255, verbose_name="Название блока")
    text = models.TextField(verbose_name="Текст блока") 

    class Meta:
        verbose_name = "Информационный блок"
        verbose_name_plural = "Информационные блоки"

    def __str__(self):
        return self.name