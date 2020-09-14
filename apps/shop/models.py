from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from apps.core.models import NameSlug, ModelImages
from apps.core.function.functions__image import tempImagePath, imageResize
from colorfield.fields import ColorField
from unidecode import unidecode
from django.utils import timezone
from project import settings
import os, PIL, io, json
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import JSONField
from ckeditor.fields import RichTextField
from apps.core.models import metaTags
import re

# Globals



class Category(NameSlug):
    name =            models.CharField(max_length=300, blank=False, unique=True, verbose_name="Название категории")
    in_catalogue =     models.BooleanField(default=False, verbose_name="Показывать на витрине по умолчанию")
    in_recomendation = models.BooleanField(default=False, verbose_name="Предлагать в рекомендованные")

    class Meta:
        ordering = ['name']
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def save(self):
        self.name = re.sub(r'[^0-9a-zA-Zа-яА-Я-_ ,]',"", self.name) 
        super(Category, self).save()

    


class Color(NameSlug, ModelImages):
    name =       models.CharField(max_length=300, blank=False, unique=True, verbose_name="Название цвета")
    image =      models.ImageField(blank=True, null=True, upload_to='', verbose_name="Фото цвета")
    image_thmb = JSONField(editable=False, null=True, blank=True, default=dict)
    hex =        ColorField(verbose_name="Код цвета", unique=True, default=None, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Цвет товара"
        verbose_name_plural = "Цвета товаров"

    def __str__(self):
        return self.name

    def clean(self):
       
        if not self.image and not self.hex:  # This will check for None or Empty
            raise ValidationError({
                'image' : 'Загрузите фото цвета',
                'hex': 'или выберите его код.'
            })


class WhoIntended(NameSlug):
    name =  models.CharField(max_length=300, blank=False, unique=True, verbose_name="Название")

    class Meta:
        ordering = ['name']
        verbose_name = "Кому предназначен"
        verbose_name_plural = "Кому предназначен"


class GiftReason(NameSlug):
    name =  models.CharField(max_length=300, blank=False, unique=True, verbose_name="Название")

    class Meta:
        ordering = ['name']
        verbose_name = "Повод для подарка"
        verbose_name_plural = "Повод для подарка"


class ProductStatus(NameSlug):
    name =  models.CharField(max_length=300, blank=False, unique=True, verbose_name="Название")
    hex =  ColorField(verbose_name="Код цвета", default="#000000") 

    class Meta:
        ordering = ['name']
        verbose_name = "Статус товара"
        verbose_name_plural = "Статус товара"



class Product(metaTags, ModelImages,):
    name =           models.CharField(max_length=255, verbose_name="Название")
    code =           models.CharField(unique=True, max_length=255, verbose_name="Артикул")
    slug =           models.SlugField(max_length=255, editable=False, null=True, blank=True)
    price =          models.PositiveIntegerField(verbose_name="Цена")
    old_price =      models.PositiveIntegerField(verbose_name="Прежняя цена", null=True, blank=True)
    discount =       models.PositiveIntegerField(verbose_name="Размер скидки", null=True, blank=True)
    category =       models.ManyToManyField(Category,      verbose_name="Категория товаров",  related_name="product", blank=True)
    who_intended =   models.ManyToManyField(WhoIntended,   verbose_name="Кому предназначен", related_name="product", blank=True)
    gift_reason =    models.ManyToManyField(GiftReason,    verbose_name="Повод для подарка", related_name="product", blank=True)
    status =         models.ManyToManyField(ProductStatus, verbose_name="Статус товара",     related_name="product", blank=True)
    in_sell =        models.BooleanField(default=True, verbose_name="В продаже")
    is_popular =     models.BooleanField(default=False, verbose_name="Популярный")
    image =          models.FileField(blank=True, null=True, upload_to='', verbose_name="Карточка товара (основная)")
    image_thmb =     JSONField(editable=True, null=True, blank=True, default=dict)
    add_image =      models.FileField(blank=True, null=True, upload_to='', verbose_name="Карточка товара (дополнительная)")
    add_image_thmb = JSONField(editable=True, null=True, blank=True, default=dict)
    length =         models.PositiveIntegerField(verbose_name="Длина (см)",  null=True, blank=False)
    width =          models.PositiveIntegerField(verbose_name="Ширина (см)", null=True, blank=False)
    height =         models.PositiveIntegerField(verbose_name="Высота (см)", null=True, blank=False)
    weight =         models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Вес (кг)", null=True, blank=False)
    description =    RichTextField(verbose_name="Описание", null=True, blank=True)
    preferences =    RichTextField(verbose_name="Характеристики", null=True, blank=True)
    created =        models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Дата создания")
    updated =        models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Последнее изменение")

    class Meta:
        ordering = ['-created']
        verbose_name = "Список товаров"
        verbose_name_plural = "Список товаров"

    def __str__(self):
        return f'{self.name} - {self.code}'

    def get_variants(self):
        return self.variants.filter(hide=False, in_stock__gte=1)

    @property
    def get_discount(self):
        if self.old_price > self.price:
            return self.old_price - self.price
        return 0

    def get_absolute_url(self):
        variant = self.variants.all().first()
        if variant:
            return reverse('shop:product', kwargs={
                'slug' :       variant.parent.slug, 
                'product_id' : variant.parent.pk,
                'color':       variant.color.slug, 
                'variant_id' : variant.pk
            })
        else: return '/'


    @property
    def make_slug(self):
        return slugify(unidecode('-'.join([self.name, self.code])))

    def clean(self):
        if self.old_price != 0 and self.old_price != None:
            if self.old_price < self.price:
                raise ValidationError({
                    'old_price' : 'Прежняя цена не может быть ниже текущей.',
                })

    def save(self):
        if self.old_price ==  None:       self.old_price = 0
        elif self.old_price < self.price: self.old_price = 0
        
        self.discount = self.get_discount
        self.slug = self.make_slug
        self.updated = timezone.now()
        super(Product, self).save()
      
    


class Variant(ModelImages):
    parent =       models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name="variants")
    first =        models.BooleanField(default=False)
    color =        models.ForeignKey(Color,   on_delete=models.PROTECT, blank=False, null=True, related_name="variants", verbose_name="Цвет")
    photo_1 =      models.FileField(verbose_name="Фото 1")
    photo_1_thmb = JSONField(editable=False, null=True, blank=True, default=dict)
    photo_2 =      models.FileField(verbose_name="Фото 2", null=True, blank=True)
    photo_2_thmb = JSONField(editable=False, null=True, blank=True, default=dict)
    photo_3 =      models.FileField(verbose_name="Фото 3", null=True, blank=True)
    photo_3_thmb = JSONField(editable=False, null=True, blank=True, default=dict)
    photo_4 =      models.FileField(verbose_name="Фото 4", null=True, blank=True)
    photo_4_thmb = JSONField(editable=False, null=True, blank=True, default=dict)
    in_stock = models.PositiveIntegerField(default=1, verbose_name="В наличии")
    hide =     models.BooleanField(default=False)

    class Meta:
        ordering = ['-first', 'color__name']
        verbose_name = "Цвет товара"
        verbose_name_plural = "Цвета товаров"
       

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={
            'slug' : self.parent.slug, 
            'product_id' : self.parent.pk,
            'color':  self.color.slug, 
            'variant_id' : self.pk
        })

    @property
    def make_slug(self):
        if not self.parent.slug:
            self.parent.slug = self.parent.make_slug
        if self.color is not None:
            return slugify(unidecode('-'.join([self.parent.slug, self.color.name])))
        else:
            return slugify(unidecode(self.parent.slug))

    def save(self):
        self.slug = self.make_slug
        super(Variant, self).save()
        if self.first == True:
            self.parent.variants.exclude(pk=self.pk).update(first=False)
        elif len(self.parent.variants.filter(first=True)) == 0:
            self.first = True
            super(Variant, self).save()

   


