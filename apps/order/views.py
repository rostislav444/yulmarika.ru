from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.user.serializers import UserAdressSerializer
from apps.shop.models import Product, Variant
from apps.shop.cart import Cart
from apps.order.models import Order, OrderProduct
from apps.delivery.models import Delivery
from apps.coupon.models import Coupon
from apps.user.models import UserAdress
from django.http import JsonResponse
from yandex_checkout import Configuration, Payment
import json, uuid


def order_payed(request):
    order = Order.objects.last()
    for item in order.products.all():
        product = item.color
        product.in_stock -= item.quantity
        product.save()
    return ''

Configuration.account_id = 740433
Configuration.secret_key = 'test_vElK711q4bXJlKZJ1W4qTpRzwM5c8Ykwhvc6WzmbZjA'

def yandex_pay_confirm(total, description="Заказ"):
    payment = Payment.create({
        "amount": {
            "value": str(total),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.merchant-website.com/return_url"
        },
            "capture": True,
            "description": description
    }, uuid.uuid4())
    return json.loads(payment.json())


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
            for key in box.keys():
                box[key].append(getattr(product.product, key))
        # Calculate box size and weight
        order.width =  max(box['width'])
        order.height = max(box['height'])
        order.length = sum(box['length'])
        order.weight = sum(box['weight'])
        order.save()
        cart.clear()
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


def order_create(request):
    context = {'header' : False}
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
        order.save()

        context['success'] = True
        order_total = order.products_cost
        if order.free_delivery == False:
            order_total = order.products_cost + order.delivery_cost
        context['payment'] = yandex_pay_confirm(order.products_cost + order.delivery_cost)
       
    context['success'] = False
    return JsonResponse(context)
   




