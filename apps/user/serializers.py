from rest_framework import serializers
from apps.user.models import UserAdress
import json


class UserAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdress
        fields = ['pk','name','surname','phone','city','street','house','apartment','add_info', 'selected']