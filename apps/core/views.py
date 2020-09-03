from django.shortcuts import render
from apps.delivery.models import DeliveryCities
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models.functions import Lower


class SearchViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def city(self, request):
        data = request.data
        name = data['name']
        cities = DeliveryCities.objects.filter(name_lower__startswith=name.lower()).values_list('name', flat=True)[:6]
        return Response({'success' : True, 'data' : {'list' : cities, 'request' : data}}) 
        