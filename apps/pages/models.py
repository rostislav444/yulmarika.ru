from django.db import models
from apps.core.models import ModelImages
import os, PIL, io, json
from django.utils.text import slugify
from unidecode import unidecode
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import JSONField
from apps.core.models import metaTags


class Page(metaTags, ModelImages):
    name =       models.CharField(max_length=255, verbose_name="Название странциы")
    slug =       models.SlugField(max_length=255, editable=False, null=True, blank=True)
    image =      models.FileField(verbose_name="Карточка товара (основная)", null=True, blank=True)
    image_thmb = JSONField(editable=True, null=True, blank=True, default=dict)
    menu_hide =  models.BooleanField(default=True)

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
    text = RichTextField(verbose_name="Текст блока") 

    class Meta:
        verbose_name = "Информационный блок"
        verbose_name_plural = "Информационные блоки"

    def __str__(self):
        return self.name


def generate_pages():
    page_list = [
        {'name' : 'О нас',               'hide' : False},
        {'name' : 'Доставка',            'hide' : False},
        {'name' : 'Контакты',            'hide' : False},
        {'name' : 'Условия и положения', 'hide' : True},
    ]
    
    for page_data in page_list:
        try: Page.objects.get(name=page_data['name'])
        except: 
            try:
                page = Page(name=page_data['name'], menu_hide=page_data['hide'])   
                page.save()
            except: pass 


@receiver(post_delete, sender=Page, dispatch_uid="generate website pages")
def post_delete_generate_pages(sender, instance, **kwargs):
    generate_pages()

@receiver(post_save, sender=Page, dispatch_uid="generate website pages")
def post_delete_generate_pages(sender, instance, **kwargs):
    generate_pages()