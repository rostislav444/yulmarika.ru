from .models import Product, Variant, WhoIntended, GiftReason, Color
from rest_framework import serializers
from project.settings import MEDIA_URL
import json


class FilterSerializer(serializers.Serializer):
    pk =       serializers.IntegerField()
    name =     serializers.CharField()
    slug =     serializers.CharField()
    selected = serializers.BooleanField(default=False)




class WhoIntendedSeriaziler(serializers.ModelSerializer):
    selected = serializers.BooleanField()

    class Meta:
        model = Product
        fields = ['pk','name','slug','selected']


class GiftReasonSeriaziler(serializers.ModelSerializer):
    selected = serializers.BooleanField()

    class Meta:
        model = GiftReason
        fields = ['pk','name','slug','selected']

class ColorSeriaziler(serializers.ModelSerializer):
    selected = serializers.BooleanField()

    class Meta:
        model = Color
        fields = ['pk','name','slug','selected']



class ProductSeriaziler(serializers.ModelSerializer):
    image =     serializers.SerializerMethodField()
    add_image = serializers.SerializerMethodField()
    status =    serializers.SerializerMethodField()
    url =       serializers.CharField(source="get_absolute_url")

    class Meta:
        model = Product
        fields = ['pk','name','slug','price','old_price','image','add_image','status','url','length','width','height','weight']

    def get_image(self, obj):
        if 'image' in obj.imgs:
            return obj.imgs['image']
        return '/'

    def get_add_image(self, obj):
        if 'add_image' in obj.imgs.keys():
            return obj.imgs['add_image']
        return ''

    def get_status(self, obj):
        ststus = []
        for status in obj.status.all():
            ststus.insert(0,{'name':status.name, 'color':status.hex})
        return ststus
    


class CartVaraintSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="parent.name")
    code = serializers.CharField(source="parent.code")
    slug = serializers.CharField(source="parent.slug")
    price = serializers.CharField(source="parent.price")
    old_price = serializers.CharField(source="parent.old_price")
    url = serializers.CharField(source="get_absolute_url")
    image = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    product_id = serializers.CharField(source="parent.pk")
    variant_id = serializers.CharField(source="pk")
    
    
    length =  serializers.IntegerField(source="parent.length")
    width =   serializers.IntegerField(source="parent.width")
    height =  serializers.IntegerField(source="parent.height")
    weight =  serializers.IntegerField(source="parent.weight")
   

    class Meta:
        model = Variant
        fields = [
            'pk','name','code','slug','color',
            'price','old_price','image','url',
            'product_id','variant_id',
            'length','width','height','weight', 'in_stock'
        ]

    def get_image(self, obj):
        thmbs = obj.imgs
        if type(thmbs) is not dict:
            thmbs = json.loads(thmbs)
        if 'photo_1' in thmbs:
            return thmbs['photo_1']['s']
        return '/static/img/no_image.jpg'

    def get_color(self, obj):
        if obj.color.image:
            return f"background-image: url({ obj.color.imgs['image']['xs'] })"
        return f"background-color: { obj.color.hex }" 


class CartProductSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="get_absolute_url")
    image = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    variant_id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'pk','name','code','slug',
            'price','old_price','image','url',
            'product_id','variant_id',
            'length','width','height','weight'
        ]

    def get_image(self, obj):
        for image in obj.imgs.values():
            if 's' in image.keys():
                return image['s']
        return '/static/img/no_image.jpg'

    def get_product_id(self, obj):
        return obj.pk

    def get_variant_id(self, obj):
        return None
