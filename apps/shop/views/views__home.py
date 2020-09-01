from django.shortcuts import render
from django.db.models import BooleanField
from django.template import Template
from apps.banner.models import Banner
from apps.shop.models import Category, Product, Variant, WhoIntended, GiftReason, Color
from apps.shop.serializers import ProductSeriaziler, WhoIntendedSeriaziler, GiftReasonSeriaziler, ColorSeriaziler, FilterSerializer
from django.http import JsonResponse
import json
import time
import random
from project import settings
import os, PIL, io, json
import math
from django.db.models import F, Value, Case, When


def add_products():
    s = """
    Что такое Lorem Ipsum?Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus PageMaker, в шаблонах которых используется Lorem Ipsum.Почему он используется?Давно выяснено, что при оценке дизайна и композиции читаемый текст мешает сосредоточиться. Lorem Ipsum используют потому, что тот обеспечивает более или менее стандартное заполнение шаблона, а также реальное распределение букв и пробелов в абзацах, которое не получается при простой дубликации "Здесь ваш текст.. Здесь ваш текст.. Здесь ваш текст.." Многие программы электронной вёрстки и редакторы HTML используют Lorem Ipsum в качестве текста по умолчанию, так что поиск по ключевым словам "lorem ipsum" сразу показывает, как много веб-страниц всё ещё дожидаются своего настоящего рождения. За прошедшие годы текст Lorem Ipsum получил много версий. Некоторые версии появились по ошибке, некоторые - намеренно (например, юмористические варианты).
    """.replace('"','').replace('.','').replace(',','').replace('?','').split(' ')

    # models = [Category, WhoIntended, GiftReason]

    # for cat in set(s):
    #     model = models[random.randint(0, len(models)-1)]
    #     print(model)
    #     obj = model(name = cat)
    #     obj.save()

    category_list = list(Category.objects.all())
    who_intended = list(WhoIntended.objects.all())
    gift_reason = list(GiftReason.objects.all())
    colors = list(Color.objects.all())

    for n in range(0, 100):
        name = ''
        for i in range(0, random.randint(3, 5)):
            name += ' ' + s[random.randint(1, len(s) - 1)]
        print(n)
        img_name = 'img/img_' + str(random.randint(1, 14)) + '.jpeg'
        image = PIL.Image.open(settings.MEDIA_ROOT + img_name).convert("RGB")
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        
        product = Product(
            name = name,
            code = str(random.randint(1000, 10000)),
            price = random.randint(10, 10000),
            old_price = random.randint(10, 10000),
            length = random.randint(10, 50),
            width = random.randint(10, 50),
            height = random.randint(10, 50),
            weight = random.randint(1, 8),
        )
        product.save()
        product.image.save(img_name, image_io)
        product.category.add(*list(set([category_list[random.randint(1, len(category_list) - 1)] for n in range(1,3)])))
        product.who_intended.add(*list(set([who_intended[random.randint(1, len(who_intended) - 1)] for n in range(1,3)])))
        product.gift_reason.add(*list(set([gift_reason[random.randint(1, len(gift_reason) - 1)] for n in range(1,3)])))
        product.save()

        
        # for color in random.sample(colors, random.randint(1, len(colors))):
        #     variant = Variant(
        #         parent = product,
        #         color = color,
        #         in_stock = random.randint(1, 10),
        #     )
        #     variant.save()
        #     for photo in ['photo_1','photo_2','photo_3']:
        #         img_name = 'img/img_' + str(random.randint(1, 14)) + '.jpeg'
        #         image = PIL.Image.open(settings.MEDIA_ROOT + img_name).convert("RGB")
        #         image_io = io.BytesIO()
        #         image.save(image_io, format='JPEG')
        #         getattr(variant, photo).save(img_name, image_io)
        #     variant.save()








   
def home(request, category=None):
    # add_products()
    page, on_page = 1, 12
   
    context, fltr = {'selected' : {}}, {}
    sort_by = [
        {'key' : 'price',    'name' : 'По цене',           'arg' : '-price'},
        {'key' : 'popular',  'name' : 'По поппулярности',  'arg' : None},
        {'key' : 'discount', 'name' : 'По размеру скидки', 'arg' : 'discount'},
        {'key' : 'date',     'name' : 'Новинки',           'arg' : '-date'},
        {'key' : 'default',  'name' : 'По умолчанию',      'arg' : None},
    ]

    if category:
        categories = category.split('&')
        fltr['category__slug__in'] = categories
        context['selected']['categories'] = categories

    products =     Product.objects.filter(in_sell=True, variants__isnull=False, **fltr).distinct()
    variants =     Variant.objects.filter(parent__in=products)
 
    

    context['filters'] = [
        {
            'name' : 'Кому', 
            'slug' : 'who_intended',
            'objects' : WhoIntended.objects.filter(product__in=products).distinct(),
            'selected' : []
        },
        {
            'name' : 'Повод', 
            'slug' : 'gift_reason',
            'objects' : GiftReason.objects.filter(product__in=products).distinct(),
            'selected' : []
        },
        {
            'name' : 'Цвет', 
            'slug' : 'color',
            'objects' : Color.objects.filter(variants__in=variants).distinct(),
            'selected' : []
        }
    ]
    
    if products.first() is not None:
        context['max_price'] =  products.order_by('-price').first().price
        context['min_price'] =  products.order_by('price').first().price
    

    if request.method == 'POST':
        product_filter = {}
        data = json.loads(request.body.decode('utf-8'))

        # Add selected ids to queryser kwargs (**product_filter) and
        # to fiter['selected'] for serializer selected True or False
        for fltr in context['filters']:
            key = fltr['slug']
            if data.get(key):
                value = [int(pk) for pk in data[key]] 
                if key in ['color']:
                    product_filter[f"variants__{key}__pk__in"] = value
                else:
                    product_filter[f"{key}__pk__in"] = value
                fltr['selected'] = value
        # Prepere data for filtering and annonantion
        for key, value in data.items():
            if key in ['price__gte','price__lte']:
                try: product_filter[key] = int(value)
                except: pass
            elif key == 'sort_by':
                if value == 'price':
                    products = products.order_by('price')
                elif value == 'date':

                    products = products.order_by('-created')
        products = products.filter(**product_filter)
        products_len = len(products)
        pages = math.ceil(products_len / 12)
     
        # Annonante selected filed for selected filter objects
        for fltr in context['filters']:
            fltr['objects'] = fltr['objects'].annotate(selected=Case(
                When(pk__in=fltr['selected'], 
                then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ))
            fltr['objects'] = FilterSerializer(fltr['objects'].order_by('-selected'), many=True,).data

        # Pagisntion / display products
        if 'display' in data.keys():
            page = int(data['page'])
            n = page * 12
            products = products[n:n + 12]
            if page + 1 <= pages:
                context['page'] = page + 1
        elif 'page' in data.keys():
            page = int(data['page'])
            context['page'] = page
            pages = math.ceil(products_len / 12)
            n = int(data['page']) - 1
            products = products[n:n + 12]
        else: products = products[:12]


        
        context['more']  = True if products_len > page * on_page else False
        context['products'] = json.loads(json.dumps(ProductSeriaziler(products, many=True).data))
        context['products_len'] = products_len
        context['pages'] = math.ceil(products_len / 12)
        return JsonResponse(context)


    products_len = len(products)
    context['more']  = True if products_len > page * on_page else False
    context['products'] = json.loads(json.dumps(ProductSeriaziler(products[:12], many=True).data))
    context['products_len'] = products_len
    context['pages'] = math.ceil(context['products_len'] / 12)
    context['categories'] = Category.objects.filter(product__variants__isnull=False).distinct()
    context['banners'] = Banner.objects.all()
    context['sort_by'] = sort_by
    return render(request, 'shop/home/home.html', context)