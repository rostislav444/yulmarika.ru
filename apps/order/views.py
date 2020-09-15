from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.user.serializers import UserAdressSerializer
from apps.shop.models import Product, Variant
from apps.shop.cart import Cart
from apps.user.serializers import UserSerializer
from apps.shop.serializers import ProductSeriaziler
from apps.order.models import Order, OrderProduct, YandexResponse
from apps.delivery.models import Delivery
from apps.coupon.models import Coupon
from apps.user.models import UserAdress
from django.http import JsonResponse
from yandex_checkout import Payment
import json, random, uuid, math
from django.views.decorators.csrf import csrf_exempt




def yandex_pay_confirm(request, total, uid, pk, description="Заказ"):
    base_url = f"{request.scheme}://{request.META.get('HTTP_HOST')}"
    path = reverse('order:confirmation', kwargs={'uid' : uid})
    payment = Payment.create({
        "amount": {
            "value": str(total),
            "currency": "RUB"
        },
        "metadata":{
            'id' : pk,
        },
        "confirmation": {
            "type": "redirect",
            "success_url" : f"{base_url}{path}",
            "return_url": f"{base_url}{path}" ,
        },
            "capture": True,
            "description": description
    }, uid)
    return json.loads(payment.json())


def confirmation(request, uid):
    order = Order.objects.filter(uid=uid).first()
    if order:
        return redirect(reverse('order:success', kwargs={'pk' : order.pk}))
    else:
        return redirect("/")





@csrf_exempt
def yandex_response(request):
    data = json.loads(request.body.decode('utf-8'))
    resposne = YandexResponse(data=data)
    resposne.save()

    try:
        order = Order.objects.get(pk=int(data['object']['metadata']['id'])) 
        order.status = 'payed'
        order.payed = timezone.now()
        order.save()
    except: pass

    for item in order.products.all():
        variant = item.variant
        variant.in_stock = max(0, variant.in_stock - item.quantity) 
        variant.save()
    
    return JsonResponse({'status' : True})

    

def order_sucess(request, pk=None):
    context = {}
    if pk:
        context['order'] = Order.objects.filter(pk=pk).first()
    recomendations = list(Product.objects.filter(category__in_recomendation=True))
    context['recomendations'] = ProductSeriaziler(random.sample(recomendations, len(recomendations))[:24], many=True).data
    context['recomendation_title'] = "Вас также могут заинтересовать:"
    return render(request, 'shop/order/success.html', context)


def save_order(request):
    cart = Cart(request)
    cart_data = cart.data()

    try:    free_delivery = int(cart_data['total']) > FileCodes.objects.last().free_delivery 
    except: free_delivery = False

    if len(cart_data['products']):
        try:    coupon = Coupon.objects.get(pk=int(request.session['coupon']))
        except: coupon = None

        order_data = {
            'products_cost' : cart_data['total'],
            'discount_cost' : cart_data['coupon_discount'] if 'coupon_discount' in cart_data else 0,
            'free_delivery' : free_delivery,
            'coupon' : coupon
        }

        try:    order = Order.objects.get(pk=int(request.session.get('order')))
        except: order = Order(status="new")
        
        for key, value in order_data.items():
            setattr(order, key, value)
        
                
        if request.user.is_authenticated:
            order.customer = request.user
            order.email =    request.user.email
            order.customer_name = f'{request.user.name} {request.user.surname}'
        order.save()

        order.products.all().delete()

        box = {'width' : [], 'height' : [], 'weight' : [], 'length' : [], }        
        for item in cart_data['products']:
            product = Product.objects.get(pk=int(item['product_id']))
            variant = Variant.objects.get(pk=int(item['variant_id']))
            color =   variant.color if variant else None
            
            product = OrderProduct(
                parent =   order,
                product =  product,
                variant =  variant,
                color =    color,
                name =     item['name'],
                price =    item['price'],
                code =     item['code'],
                quantity = item['quantity'],
            )
            product.save()
            for i in range(int(product.quantity)):
                for key in box.keys():
                    box[key].append(getattr(product.product, key))
               
        # Calculate box size and weight
        order.width =  max(box['width'])
        order.height = max(box['height'])
        order.length = sum(box['length'])
        order.weight = math.ceil(sum(box['weight']))
       
        order.save()
        
        request.session['order'] = order.pk
    return request.session['order'] if 'order' in request.session.keys() else None
    


def order_or_register(request):
    if request.user.is_authenticated:
        return redirect(reverse('order:create'))
    return redirect(reverse('user:auth_register_or_order'))


def order_data(request):
    return ''

def order(request):
    cart = Cart(request).data()
    if len(cart['products']):
        return render(request, 'shop/order/order.html')
    return redirect('/')


def order_decline(request, order_pk):
    if request.user.is_authenticated:
        user = request.user
        order = user.orders.filter(pk=order_pk).first()
        if order:
            order.status = 'declined'
            order.save()
        return redirect(reverse('user:profile_orders'))
    else:
        return redirect(reverse('user:login'))


def order_description(order):
    total = order.products_cost
    if order.free_delivery == False:
        total = order.products_cost + order.delivery_cost
    description = f"Оплата заказа №{ order.order_id } в магазине Юлмарика"
    return total, description


def order_create(request, order_pk=None):
    context = {
        'header' : False,
    }
    if request.user.is_authenticated:
        context['user_data'] = json.dumps(UserSerializer(request.user).data)
    else: 
        context['user_data'] = json.dumps({})

    if order_pk:
        if request.user.is_authenticated:
            order = Order.objects.filter(pk=order_pk, customer=request.user).first()
        else:
            order = Order.objects.filter(pk=order_pk, customer=None).first()
        if order:
            if order.delivery_cost == 0:
                context['order'] = order
                return render(request, 'shop/order/order_create.html', context)
            else:
                total, description = order_description(order)
                response = yandex_pay_confirm(request, total, order.uid, order.pk, description)
                return redirect(response["confirmation"]["confirmation_url"])
    else:
        order_pk = save_order(request)
        if order_pk:
            context['order'] = Order.objects.get(pk = order_pk)
            return render(request, 'shop/order/order_create.html', context)

    return redirect('/')


def make_order(request):
    context = {}
    order = Order.objects.filter(pk=request.session['order'] if 'order' in request.session.keys() else 0).first()
    if order:
        if request.user.is_authenticated:
            order.customer = request.user
            try:    adress = request.user.adress.get(selected=True)
            except: adress = request.user.adress.all().first()
            if adress:
                order.customer_name = f'{adress.name} {adress.surname}'
                order.phone = adress.phone
                order.adress = f'{adress.city}, {adress.street} д.{adress.house} кв.{adress.apartment}'
                order.comments = adress.add_info
            else:
                context['success'] = False
                context['msg'] = "Адресов не найдено"
                return JsonResponse(context)
            
        else:
            adress = request.session['adress'][0]
            order.customer = None
            order.customer_name = f"{adress['name']} {adress['surname']}"
            order.phone = adress['phone']
            order.adress = f"{adress['city']}, {adress['street']} д.{adress['house']} кв.{adress['apartment']}"
            order.comments = adress['add_info']

        

        session = request.session
        data = json.loads(request.body.decode('utf-8'))
        delivery = {"ruspost" : "Почта России", "cdek" : "CDEK"}
        order.delivery_type = delivery[data['delivery']]
        order.delivery_cost = session['delivery'][data['delivery']]
        order.status = 'created'
        order.uid = uuid.uuid4()
        order.save()

        context['success'] = True

        coupon = order.coupon
        if coupon and coupon.once:
            orders = Order.objects.filter(coupon=coupon)
            if len(orders) > 1:
                if coupon.used == False:
                    orders = orders.exclude(pk=order.pk)
                for ordr in orders:
                    ordr.products_cost = order.initial_cost
                    ordr.coupon = None
                    ordr.save()

        total, description = order_description(order)
        context['payment'] = yandex_pay_confirm(request, total, order.uid, order.pk, description)
       
    context['success'] = False
    return JsonResponse(context)
   




