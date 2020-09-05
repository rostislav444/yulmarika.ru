from django.shortcuts import render
from django.http import JsonResponse
from apps.shop.cart import Cart
from .models import Coupon
import json


def coupon_activate(request, coupon):
    cart = Cart(request)
    cart_data = cart.data()
    if coupon.expired:
        return JsonResponse({'success' : False, 'msg' : 'Срок действия купона истек'})
    if coupon.used:
        return JsonResponse({'success' : False, 'msg' : 'Купон уже использован'})
    if cart_data['total'] < coupon.minimum:
        return JsonResponse({'success' : False, 'msg' : f'Минимальная сумма для использования купона - {coupon.minimum} RUB'})
    
    request.session['coupon'] = coupon.pk
    return JsonResponse({'success' : True, 'msg' : 'Купон активирован', 'cart' : cart.data()})


def coupon_check(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        coupon = Coupon.objects.get(text=data['text'])
        return coupon_activate(request, coupon)
    except:
        return JsonResponse({'success' : False, 'msg' : 'Такого купона не существует'})
