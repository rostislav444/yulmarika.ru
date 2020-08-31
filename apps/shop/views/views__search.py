from django.shortcuts import render
from apps.shop.serializers import ProductSeriaziler
from Levenshtein import StringMatcher as sm
from apps.shop.models import Product, Variant
from django.http import JsonResponse
from fuzzywuzzy import fuzz
from operator import itemgetter
import json, math





def search(request):
    search_input = request.GET['input']
   
    products = []
    context = {}
    if search_input:
        def match(inpt,val):
            length = len(inpt.split(' '))
            vals = val.split(' ')
            for n in range(0,len(vals)):
                analog = ' '.join(vals[n:length+n])
                ratio = fuzz.ratio(inpt,analog)
                if inpt in val:
                    return 100
                if ratio > 80:
                    return ratio
            return 0

        for product in list(Product.objects.all()):
            ratio = match(search_input,product.name)
            if ratio >= 80:
                prod = ProductSeriaziler(product).data
                prod['ratio'] = ratio
                products.append(prod) 
        
        products = sorted(products, key=itemgetter('ratio'))
      
        context['search_input'] = search_input
        context['products_len'] = len(products)
        context['pages'] = math.ceil(context['products_len'] / 12)
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            if 'display' in data.keys():
                page = int(data['page'])
                n = page * 12
                products = products[n:n + 12]
                if page + 1 <= context['pages']:
                    context['page'] = page + 1
            elif 'page' in data.keys():
                context['page'] = int(data['page'])
                pages = math.ceil(context['products_len'] / 12)
                n = (int(data['page']) - 1) * 12 
                products = products[n:n + 12]
            else:
                products = products[:12]

            context['products'] = products
            return JsonResponse(context)

        context['products'] = json.loads(json.dumps(products[:12]))
    return render(request, 'shop/search_result.html', context)
