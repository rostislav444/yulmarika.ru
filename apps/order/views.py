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
from apps.order.models import Order, OrderProduct
from apps.delivery.models import Delivery
from apps.coupon.models import Coupon
from apps.user.models import UserAdress
from django.http import JsonResponse
from yandex_checkout import Configuration, Payment
import json, random, uuid, math


Configuration.account_id = 740433
Configuration.secret_key = 'test_vElK711q4bXJlKZJ1W4qTpRzwM5c8Ykwhvc6WzmbZjA'

def yandex_pay_confirm(request, total, uid, description="Заказ"):
    base_url = f"{request.scheme}://{request.META.get('HTTP_HOST')}"
    path = reverse('order:confirmation', kwargs={'uid' : uid})
    payment = Payment.create({
        "amount": {
            "value": str(total),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{base_url}{path}" 
        },
            "capture": True,
            "description": description
    }, uuid.uuid4())
    return json.loads(payment.json())


def confirmation(request, uid):
    Cart(request).clear()
    
    order = Order.objects.filter(uid=uid).first()
    if order:
        order.uid = ''
        order.status = 'payed'
        order.payed = timezone.now()
        order.save()
        return redirect(reverse('order:success'))
    else:
        return redirect("/")


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
    if len(cart_data['products']):
        try:    coupon = Coupon.objects.get(pk=int(request.session['coupon']))
        except: coupon = None
        order = Order(
            status = "new",
            products_cost = cart_data['total'],
            discount_cost = cart_data['coupon_discount'] if 'coupon_discount' in cart_data else 0,
            coupon = coupon,
        )
        if coupon:
            if coupon.once:
                coupon.used = True
                coupon.save()
                
        if request.user.is_authenticated:
            order.customer = request.user
            order.email =    request.user.email
            order.customer_name = f'{request.user.name} {request.user.surname}'
        order.save()
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

   

def order_create(request, order_pk=None):
    context = {
        'header' : False,
    }
    if request.user.is_authenticated:
        context['user_data'] = json.dumps(UserSerializer(request.user).data)
    else: context['user_data'] = json.dumps({})


    if order_pk and request.user.is_authenticated:
        user = request.user
        order = user.orders.filter(pk=order_pk).first()
        if order:
            if order.delivery_cost > 0:
                order_total = order.products_cost
                if order.free_delivery == False: 
                    order_total += order.delivery_cost

                response = yandex_pay_confirm(order.products_cost + order.delivery_cost)
                return redirect(response["confirmation"]["confirmation_url"])
            else:
                context['order'] = order
                return render(request, 'shop/order/order_create.html', context)
                

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

        description = ''
        for n, item in enumerate(order.products.all()):
            name = item.product.name
            color = item.color.name
            price = item.product.price
            qty  = item.quantity
            description += f'{n}. {name} - {color}, {qty} шт. * {price} RUB \n'

        session = request.session
        data = json.loads(request.body.decode('utf-8'))
        delivery = {"ruspost" : "Почта России", "cdek" : "CDEK"}
        order.delivery_type = delivery[data['delivery']]
        order.delivery_cost = session['delivery'][data['delivery']]
        order.status = 'created'
        order.uid = uuid.uuid1()
        order.save()

        context['success'] = True
        total = order.products_cost
        if order.free_delivery == False:
            total = order.products_cost + order.delivery_cost
        description = 'Всего c доставкой: ' + str(total)
        context['payment'] = yandex_pay_confirm(request, total, order.uid, description)
       
    context['success'] = False
    return JsonResponse(context)
   




