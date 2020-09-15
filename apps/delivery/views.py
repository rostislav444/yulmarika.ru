from django.shortcuts import render
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.user.serializers import UserAdressSerializer
from apps.shop.cart import Cart
from apps.order.models import Order
from apps.delivery.models import Delivery
from apps.coupon.models import Coupon
from apps.user.models import UserAdress
from apps.filecodes.models import FileCodes
import json




class UserAdressViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_adress_data(self, request):
        adress_list = []
        if request.user.is_authenticated:
            for adress in request.user.adress.all():
                adress_list.append(UserAdressSerializer(adress).data)
        else:
            if 'adress' in request.session.keys():
                adress_list = request.session['adress']

        
        delivery = self.dlivery_price(request)
      
        response = {
            'success' : True,
            'data' : {
                'adress_list' : adress_list,
                'delivery' : delivery,
            }
        }
        return response

   
    def save_adress(self, request, id=None):
        data = {}

        for field in UserAdress._meta.get_fields():
            try: data[field.name] = request.data[field.name]
            except: pass
        
        if request.user.is_authenticated:
            adress_list = []
            UserAdress.objects.filter(user=request.user).update(selected=False)
            if 'id' in data.keys():
                adress = UserAdress.objects.filter(pk=int(data['id'])).update(selected=True, **data) 
            else:
                adress = UserAdress(user=request.user, **data)
                adress.selected=True
                adress.save()
        else:
            request.session['adress'] = []
            request.session['adress'].append(data) 
           
        self.dlivery_price(request)
        return Response(self.get_adress_data(request))


    def get_adress(self, request, id=None):
        return Response(self.get_adress_data(request)) 


    def set_adress(self, request):
        adress_list = []
        adress_id = int(request.data['adress']) if 'adress' in request.data.keys() else None
        if request.user.is_authenticated:
            if adress_id:
                request.user.adress.all().update(selected=False)
                request.user.adress.filter(pk=adress_id).update(selected=True)
            for adress in request.user.adress.all():
                adress_list.append(UserAdressSerializer(adress).data)
        else:
            if 'adress' in request.session.keys():
                adress_list.append(request.session['adress'])
        response = {
            'success' : True,
            'data' : {
                'adress_list' : adress_list,
                'delivery' : self.dlivery_price(request)
            }
        }
        print(response)
        return Response(response) 
        

    def dlivery_price(self, request):
        fk = FileCodes.objects.all().first()
        if fk: base_delivery_price = fk.base_delivery
        else:  base_delivery_price = 400

        session = request.session
        if 'delivery' not in session.keys(): session['delivery'] = {}
        delivery_data = { 
            'ruspost' : [], 'cdek' : [] 
        }
        cart = Cart(request).data()
        delivery = Delivery.objects.first()
        order = Order.objects.filter(pk=session['order'] if 'order' in session.keys() else 0).first()
        
        if order:
            data = {
                'key' : delivery.api_key,
                'q' : 'getPrice',
                'arrivalDoor' : True,
                'derivalDoor' : True,
                'startCity' : 'Челябинск',
                'weight' : int(order.weight),
                'width' :  int(order.width),
                'height' : int(order.height),
                'length' : int(order.length),
            }
            response = None
            if request.user.is_authenticated:
                adress_list = request.user.adress.all()
              
                if len(adress_list):
                    try:    city = adress_list.get(selected=True).city
                    except: city = adress_list[0].city
                    data['endCity'] = city
                    response = delivery.send_request(data)
            else:

                adress_list = request.session.get('adress')
                if adress_list:
                    data['endCity'] = adress_list[0]['city']
                    response = delivery.send_request(data)

            if response:
                if type(response) == list:
                    for item in response:
                        if   item['name'] == 'CDEK':         delivery_data['cdek'].append(item['price'])
                        elif item['name'] == 'Почта России': delivery_data['ruspost'].append(item['price'])
                else:
                    delivery_data['ruspost'].append(base_delivery_price)
                    
            


        delivery_data['ruspost'] = min(delivery_data['ruspost']) if len(delivery_data['ruspost']) else 0
        delivery_data['cdek'] =    min(delivery_data['cdek'])    if len(delivery_data['cdek'])    else 0
        request.session['delivery'] = delivery_data
        return delivery_data
