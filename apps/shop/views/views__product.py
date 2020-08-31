from django.shortcuts import render
from apps.shop.models import Category, Product, Variant
from apps.shop.serializers import ProductSeriaziler
import random

def product(request, slug, product_id, color=None, variant_id=None):
    recomendations = list(Product.objects.filter(category__in_recomendation=True))
   
    context = {
        'product' : Product.objects.get(pk=int(product_id)),
        'variant' : Variant.objects.get(pk=int(variant_id)) if variant_id else None,
        'recomendations' : ProductSeriaziler(random.sample(recomendations, len(recomendations))[:24], many=True).data
    }

    
    return render(request, 'shop/product/product.html', context)