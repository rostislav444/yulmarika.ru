from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from apps.user.models import CustomUser, UserAdress
from apps.user.serializers import UserAdressSerializer
from apps.delivery.models import Delivery
from project import settings
import json, os, re
from apps.shop.cart import Cart
import datetime
from django.utils.safestring import SafeString
from django.contrib.auth import logout


def auth_register_or_order(request):
    if request.user:
        if user.is_authenticated():
            return redirect(reverse('order:create'))
    return render(request, 'user/auth_register_or_order.html')


class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def auth(self, request):
        data = request.data
        redirect = data['redicrect'] if 'redicrect' in data.keys() else "/"
        try:     
            user = CustomUser.objects.get(email=data["email"])
        except: 
            return Response({'success' : False, 'msg' : f'Пользователь с Email: {data["email"]}, не зарегестрирован.'})
        user = authenticate(request, username=data['email'], password=data['password'])
        if user is not None:
            login(request, user)
            return Response({'success' : True,  'msg' : 'Вы авторизованы.', 'redirect' : redirect})
        else:
            return Response({'success' : False, 'msg' : 'Пароль введен не правильно.'})
    
    def register(self, request):
        data = request.data
        try:     
            user = CustomUser.objects.get(email=data["email"])
            return Response({'success' : False, 'msg' : f'Пользователь с Email: {data["email"]}, уже зарегестрирован.'})
        except: 
            try:
                user = CustomUser.objects.create_user(
                    email = data["email"],
                    password = data["password"],
                    data = {
                        "name" :    data["name"],
                        "surname" : data["surname"],
                    },
                )
                user = authenticate(request, username=data['email'], password=data['password'])
                if user is not None:
                    login(request, user)
                
                return Response({'success' : True,  'msg' : 'Вы зарегистрированы в системе', 'redirect' : '/'})
            except:
                return Response({'success' : False, 'msg' : 'Произошла ошибка'})




class UserProfile(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def orders(self, request):
        if request.user.is_authenticated:
            context = {'user' : request.user}
            return render(request, 'user/profile__orders.html',context)
        else:
            return redirect(reverse('user:login'))

    def data(self, request):
        errors = []
        if request.user.is_authenticated:
            context = {'user' : request.user}
            if request.method == "POST":
                data = request.data
                if 'userdata' in data.keys():
                    userQS = CustomUser.objects.filter(pk=request.user.pk)
                    user_data = data['userdata']
                    user = userQS.first()

                    email = CustomUser.objects.filter(email=user_data['email']).first()
                    if email != None and email.pk != user.pk:
                        msg = "Пользователь с таким email уже зарегестрирован на сайте"
                        errors.append(msg)

                    phone = CustomUser.objects.filter(email=user_data['phone']).first()
                    if phone != None and phone.pk != user.pk:
                        msg = f"Пользователь с таким номером телефона +7{data['phone']} уже зарегестрирован на сайте"
                        errors.append(msg)

                    
                    if len(errors) == 0:
                        user = CustomUser.objects.filter(pk=request.user.pk).update(
                            gender =   user_data['gender'],
                            name =     user_data['name'],
                            surname =  user_data['surname'],
                            email =    user_data['email'],
                            phone =    user_data['phone'],
                            birthday = datetime.datetime.strptime(user_data['birthday'], "%d.%m.%Y").date()
                        )
                if 'password' in data.keys():
                    password_data =  data['password']
                    user = CustomUser.objects.filter(pk=request.user.pk).first()

                    if not user.check_password(password_data['old_password']):
                        errors.append("Вы ввели не правильный прежний пароль")
                    else:
                        if password_data['new_password'] != password_data['new_password']:
                            errors.append("Пароли не совпадают")
                        else:
                            if re.match(r"^[0-9a-zA-Z]{6,24}$", password_data['new_password']) == False:
                                errors.append("Пароль имеет не верный формат")
                            else:
                                user.set_password(password_data['new_password'])
                                user.save()
                                login(request, user)

                return Response({'errors' : errors})
            return render(request, 'user/profile__data.html',context)
        else:
            return redirect(reverse('user:login'))
        
    def adresses(self, request):
        adress_list = UserAdressSerializer(request.user.adress, many=True).data
        context = {
            'user' : '',
            'adress_list' : adress_list,
            'adress_list_json' : SafeString(json.dumps(adress_list))
        }
        if request.method == 'POST':
            data = request.data
            UserAdress.objects.filter(user=request.user).update(selected = False)
            if len(data['id']):
                UserAdress.objects.filter(pk=int(data['id'])).update(
                    name =      data['name'],
                    surname =   data['surname'],
                    phone =     data['phone'],
                    city =      data['city'],
                    street =    data['street'],
                    house =     data['house'],
                    apartment = data['apartment'],
                    add_info =  data['add_info'],
                    selected = True,
                )
            else:
                user_adress = UserAdress(
                    user =      request.user,
                    name =      data['name'],
                    surname =   data['surname'],
                    phone =     data['phone'],
                    city =      data['city'],
                    street =    data['street'],
                    house =     data['house'],
                    apartment = data['apartment'],
                    add_info =  data['add_info'],
                    selected = True,
                )
                user_adress.save()
            adress_list = UserAdress.objects.filter(user=request.user)
            adress_list = UserAdressSerializer(adress_list, many=True).data
            return Response({'success' : True, 'data': adress_list})

        return render(request, 'user/profile__adress.html',context)

    def exit(self, request):
        logout(request)
        return redirect('/')



