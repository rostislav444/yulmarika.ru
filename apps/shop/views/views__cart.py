from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.shop.models import Product, Variant
from apps.shop.cart import Cart
from project import settings
import re, json




class CartViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def initial(self, request, *args, **kwargs):
        self.cart = Cart(request)
        super(CartViewSet, self).initial(request, *args, **kwargs)

    def data(self, request):
        data = self.cart.data()
        return Response(data)
    
    def add(self, request):
        data = self.cart.add(**request.data)
        return Response(data)

    def remove(self, request):
        data = self.cart.remove(**request.data)
        return redirect('shop:cart_data')

    def clear(self, request):
        return redirect('shop:cart_data')

    def fast_buy(self, request, product_id, variant_id=None):
        self.cart.add( 
            product_id = product_id,
            variant_id = variant_id,
            quantity = 1,
            update=True,
        )
        return redirect('order:cart')
