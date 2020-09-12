from django.shortcuts import render, redirect
from apps.shop.models import Category, Product, Variant
from apps.filecodes.models import FileCodes
from apps.shop.serializers import ProductSeriaziler
import random

def product(request, slug, product_id, variant_id, color=None):
    recomendations = list(Product.objects.filter(category__in_recomendation=True))
    fk = FileCodes.objects.last()
    try: on_page = fk.recomend
    except: on_page = 24

    product = Product.objects.get(pk=int(product_id))
    variant = Variant.objects.get(pk=int(variant_id))
    if variant.hide or variant.in_stock < 1:
        variant = product.variants.filter(hide=False, in_stock__gte=1).first()
        if variant:
            return redirect(variant.get_absolute_url())
        else:
            return redirect('/')

    context = {
        'product' : product,
        'variant' : variant,
        'recomendations' : ProductSeriaziler(random.sample(recomendations, len(recomendations))[:on_page], many=True).data
    }

    
    return render(request, 'shop/product/product.html', context)