from .models import FileCodes
from apps.order.models import Order
from apps.shop.cart import Cart
import re

def fron_files(request):
    order_pk = request.session.get('order')
    if order_pk:
        order = Order.objects.filter(pk=int(order_pk), status__in=['payed','prepered','at_delivry','delivring','delivred','declined']).first()
        if order:
            Cart(request).clear()
            try: del request.session['order']
            except: pass
            try: del request.session['coupon']
            except: pass

            coupon = order.coupon
            if coupon:
                if coupon.once:
                    coupon.used = True
                    coupon.save()

    context = {
        'front_files' :  FileCodes.objects.last()
    }
    try:
        context['front_files'].phone = re.sub('[^0-9]', '', context['front_files'].phone) 
        context['favicon_ext'] = context['front_files'].favicon.name.split('.')[-1]
    except: pass
    return context