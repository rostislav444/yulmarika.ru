from rest_framework import serializers
from apps.user.models import CustomUser,UserAdress
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name','surname','phone','email']

class UserAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdress
        fields = ['pk','name','surname','phone','city','street','house','apartment','add_info', 'selected']