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


def order_or_register(request):
    if request.user.is_authenticated:
        return redirect(reverse('order:create'))
    return redirect(reverse('user:auth_register_or_order'))


def order_create(request):
    context = {'header' : False}
    return render(request, 'shop/order/order_create.html', context)


def payment(request):
    context = {}
    return render(request, 'shop/order/payment.html', context)



def order_payed(request):
    order = Order.objects.last()
    for item in order.products.all():
        product = item.color
        product.in_stock -= item.quantity
        product.save()
    return ''




def make_order(request):
    context = {}
    cart = Cart(request)
    cartData = cart.data()
    rqstData = json.loads(request.body.decode('utf-8'))
    session = request.session

    delivery = {
        "ruspost" : "Почта России",
        "cdek" : "CDEK",
    }
    delivery_type = delivery[rqstData['delivery']]
    delivery_cost = session['delivery'][rqstData['delivery']]

    try:    coupon = Coupon.objects.get(pk=int(session['coupon']))
    except: coupon = None
    
    order = Order(
        status = "new",
        products_cost = cartData['total'],
        discount_cost = cartData['coupon_discount'] if 'coupon_discount' in cartData else 0,
        delivery_cost = delivery_cost,
        delivey_type =  delivery_type,
        coupon = coupon,
    )

    if request.user.is_authenticated:
        try:
            adress = request.user.adress.get(selected=True)
        except:
            adress = request.user.adress.all()[0]
        order.customer = request.user
        order.customer_name = f'{adress.name} {adress.surname}'
        order.phone = adress.phone
        order.adress = f'{adress.city}, {adress.street} д.{adress.house} кв.{adress.apartment}'
        order.comments = adress.add_info
        
    else:
        adress = request.session['adress'][0]
        order.customer = None
        order.customer_name = f"{adress['name']} {adress['surname']}"
        order.phone = adress['phone']
        order.adress = f"{adress['city']}, {adress['street']} д.{adress['house']} кв.{adress['apartment']}"
        order.comments = adress['add_info']
    order.save()

    description = []

    for item in cartData['products']:
        product = OrderProduct(
            parent =   order,
            product =  Product.objects.filter(pk=item['product_id']).first(),
            color =    Variant.objects.filter(pk=item['variant_id']).first(),
            name =     item['name'],
            price =    item['price'],
            code =     item['code'],
            quantity = item['quantity'],
        )
        description.append(f"{item['name']} * {str(item['quantity'])}")
        product.save()

    cart.clear()

    description = '\n'.join(description)
    context['success'] = True
    context['payment'] = yandex_pay_confirm(cartData['total'], description)
    return JsonResponse(context)
   




