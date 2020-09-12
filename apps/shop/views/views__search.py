from django.shortcuts import render
from apps.shop.serializers import ProductSeriaziler
from Levenshtein import StringMatcher as sm
from apps.shop.models import Product, Variant
from django.http import JsonResponse
from fuzzywuzzy import fuzz
from operator import itemgetter
import json, math





def search(request):
    context = {}
    on_page = 12
  
    def MatchProdutcs(search_input):
        products = []
        
        def match(inp,val):
            wmtch = 0
            inps = inp.split(' ')
            vals = val.split(' ')
            for iw in inps:
                for vw in vals:
                    ratio = max([fuzz.ratio(iw,vw), fuzz.ratio(iw,vw[:len(iw)+1])])

                    if ratio > 45:
                        wmtch += ratio
                        break
                   
            return wmtch

        if search_input:
            for product in list(Product.objects.filter(in_sell=True, variants__in_stock__gte=1, variants__hide=False, variants__isnull=False).distinct()):
                ratio = match(search_input.lower(), product.name.lower())
                if ratio >= 65:
                    prod = ProductSeriaziler(product).data
                    prod['ratio'] = ratio
                    products.append(prod) 
            products = sorted(products, key=itemgetter('ratio'), reverse=True)
        
        context['products'] = json.loads(json.dumps(products))
        context['search_input'] = search_input if search_input else ''
        context['products_len'] = len(products)
        context['pages'] = math.ceil(context['products_len'] / 12)
    
        request.session['search_context'] = context.copy()
        return context

    if request.method == "GET":
        search_input = request.GET.get('input')
        context = MatchProdutcs(search_input)
        context['products'] = context['products'][:on_page]
        return render(request, 'shop/search_result.html', context)


    elif request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        context =      request.session['search_context']
        products =     context['products']
        products_len = context['products_len']
        context['more'] = False
        page = 1
       
        if 'page' in data.keys():
            page = int(data['page']) if 'page' in data else 1
            context['page'] = page
            pages = math.ceil(products_len / on_page)
            n = (int(data['page']) - 1) * on_page
            product_start = n
            product_end = n + on_page
            context['more']  = True if products_len > page * on_page else False
    
        context['products'] = products[(page - 1) * on_page :page * on_page]
        return JsonResponse(context)

       
   
