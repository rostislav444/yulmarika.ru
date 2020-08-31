from django.shortcuts import render
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.user.serializers import UserAdressSerializer
from apps.shop.cart import Cart
from apps.delivery.models import Delivery
from apps.coupon.models import Coupon
from apps.user.models import UserAdress
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

        if 'delivery' not in request.session:
            delivery = self.dlivery_price(request)
        else: 
            delivery = request.session['delivery']
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
        return Response(response) 
        

    def dlivery_price(self, request):
        session = request.session
        cart = Cart(request).data()
        delivery = Delivery.objects.first()
        if 'delivery' not in session.keys():
            session['delivery'] = {}
        delivery_data = { 
            'ruspost' : [], 
            'cdek' : [] 
        }
        if int(cart['quantity']) > 0:
            data = {
                'key' : delivery.api_key,
                'q' : 'getPrice',
                'arrivalDoor' : True,
                'derivalDoor' : True,
                'startCity' : 'Челябинск',
                'weight' : cart['weight'],
                'width' :  cart['width'],
                'height' : cart['height'],
                'length' : cart['length'],
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
                adress_list = request.session['adress']
                if len(adress_list):
                    data['endCity'] = adress_list[0]['city']
                    response = delivery.send_request(data)

            if response:
                try: print(response['err'])
                except:
                    for item in response:
                        if item['name'] == 'CDEK':
                            delivery_data['cdek'].append(item['price'])
                        elif item['name'] == 'Почта России':
                            delivery_data['ruspost'].append(item['price'])

        delivery_data['ruspost'] = min(delivery_data['ruspost']) if len(delivery_data['ruspost']) else 0
        delivery_data['cdek'] =    min(delivery_data['cdek'])    if len(delivery_data['cdek'])    else 0
        request.session['delivery'] = delivery_data
        return delivery_data
