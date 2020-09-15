from project import settings
from apps.shop.models import Product, Variant
from apps.shop.serializers import CartProductSerializer, CartVaraintSerializer
from apps.coupon.models import Coupon

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {
                'products' : [], 
                'total' : 0, 
                'quantity' : 0,
                'coupon' : None,
            }
        self.cart = cart


    def __iter__(self):
        items = []
        products = self.cart['products']
        for i, item in enumerate(products):
            try:
                product = Product.objects.get(pk = int(item['product_id']), in_sell=True)
                if item['variant_id'] is not None:
                    variant = Variant.objects.get(pk = int(item['variant_id']), hide=False, in_stock__gte=1)
                else:
                    variant = None
                items.append({'product':product, 'variant':variant, 'quantity':int(item['quantity'])})
            except:
                self.cart['products'].remove(item)
        self.save()
        
        for item in items:
            yield item


    def add(self, product_id, variant_id, quantity=1, update=False):
        products = self.cart['products']
        product = Product.objects.get(pk = int(product_id))
        product_id = product.pk
        variant = None
       
        if variant_id != None:
            variant = product.variants.get(pk = int(variant_id))
            try:
                variant = product.variants.get(pk = int(variant_id))
                variant_id = variant.pk
            except: variant_id = None
     
        num = None
        for n, item in enumerate(products):
            if item['product_id'] == product_id and item['variant_id'] == variant_id:
                num = n
                break
        if num != None:
            if update: products[num]['quantity'] = quantity
            else:      products[num]['quantity'] = int(products[num]['quantity']) + quantity
        else:
            products.append({
                'product_id' : product_id, 'variant_id' : variant_id, 'quantity' : quantity,
            })
        self.save()
        return self.data()

    def remove(self, product_id, variant_id):
        num = None
        products = self.cart['products']
        for n, item in enumerate(products):
            if item['product_id'] == product_id and item['variant_id'] == variant_id:
                num = n
                break
        del self.cart['products'][num]
        self.save()

    
    def set_coupon(self, data, id):
        try:
            self.session
            coupon = Coupon.objects.get(pk=int(id))
            if data['total'] < coupon.minimum or coupon.expired or coupon.used:
                del self.session['coupon']
                self.save()
                return data
            
            data['coupon'] = {
                'minimum' : coupon.discount,
                'unit' :    coupon.unit,
                'minimum' : coupon.minimum,
            }
            if coupon.unit == 'rub':
                data['coupon_discount'] = int(coupon.discount)
            elif coupon.unit == 'percent':
                data['coupon_discount'] = round(data['total'] * (int(coupon.discount) / 100), 0) 
            data['total_save'] += data['coupon_discount']
            data['total_initial'] = data['total']
            data['total'] -= data['coupon_discount']
        except: 
            pass
        return data
    

    def data(self):
        data = {'products' : [], 'total' : 0, 'quantity' : 0, 'total_save' : 0 }

        for item in self:
            serializer = None
            if item['variant']:
                serializer = CartVaraintSerializer(item['variant']).data 
            else:
                serializer = CartProductSerializer(item['product']).data 
            serializer['quantity'] = item['quantity']
        
            if serializer:
                price = int(serializer['price'])
                old_price = int(serializer['old_price'])
                quantity = int(item['quantity'])
                data['quantity'] += quantity
                data['total'] += quantity * price
                if old_price and old_price > price:
                    data['total_save'] += (quantity * old_price) - (quantity * price)
                data['products'].append(serializer)

        if 'coupon' in self.session.keys():
            return self.set_coupon(data, self.session['coupon'])
        return data

    

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()