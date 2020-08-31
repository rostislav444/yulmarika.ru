from django.contrib import admin
from django import forms
from .models import Order, OrderProduct
from apps.shop.models import Color

from django.utils.safestring import mark_safe


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(OrderProductForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs.keys():
            if kwargs['instance'] is not None:
                instance = kwargs['instance']
                colors = instance.product.variants.all().values_list('color', flat=True)
                self.fields['color'].queryset = Color.objects.filter(pk__in=[color for color in colors]) 


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    form = OrderProductForm
    extra = 0

    def image(self, obj=None):
        if obj.pk:
            print('OBJ', obj)
            img = mark_safe(
                """<img style="width:160px; height:160px; object-fit: contain; object-position: center; border: 1px solid #ededed;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.product.imgs['image']['s'], width=240, height=240))
            return img
        return '-'

    def color_image(self, obj=None):
        # if obj.pk:
        #     if obj.color:
        #         img = mark_safe(
        #             """<img style="width:160px; height:160px; object-fit: contain; object-position: center; border: 1px solid #ededed;" 
        #             src="{url}" width="{width}" height={height} />""".format(url = obj.color.imgs['image']['s'], width=240, height=240))
        #         return img
        return '-'

    readonly_fields = ['image','color_image']
    fields = ['image','product','name','code','quantity','price','color_image','color']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = [
        'status',
        'order_id',
        'products_cost',
        'created',
        'customer_name',
        'phone',
        'email',
        'coupon',
        'adress',
        'delivey_type',
        'delivery_cost',
    ]
    list_filter = [
        'status',
        'created',
        'delivey_type',
    ]



