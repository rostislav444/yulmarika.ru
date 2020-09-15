from django.contrib import admin
from django import forms
from .models import Order, OrderProduct, YandexResponse
from apps.shop.models import Color
from django.urls import reverse
from django.utils.safestring import mark_safe




@admin.register(YandexResponse)
class YandexResponseAdmin(admin.ModelAdmin):
    def order_id(self, obj=None):
        if obj: 
            try: return obj.data['object']['metadata']['id']
            except: pass
        return '-'

    def paid(self, obj=None):
        if obj: 
            try: return obj.data['object']['paid']
            except: pass
        return '-'

    def paid(self, obj=None):
        if obj: 
            try: return f"{obj.data['object']['amount']['value']} RUB"
            except: pass
        return '-'

     


    readonly_fileds = ['order_id','paid']
    list_display = ['time', 'order_id','paid']

    

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
            url = reverse(f'admin:{obj.product._meta.app_label}_{obj.product._meta.model_name}_change', args=[obj.product.pk])
            img = mark_safe(
                f"""<a href={url}>
                    <img style="width:120px; height:120px; object-fit: contain; object-position: center; border: 1px solid #ededed;" src="{obj.product.imgs['image']['s']}" />
                </a>""")
            return img
        return '-'

    def color_image(self, obj=None):
        if obj.pk:
            img = mark_safe(
                f"""<img style="width:120px; height:120px; object-fit: contain; object-position: center; border: 1px solid #ededed;" 
                src="{obj.variant.imgs['photo_1']['s']}"/>""")
            return img
        return '-'
    color_image.short_description = "Изображение цвета"

    def color_view(self, obj=None):
        if obj.pk:
            if obj.color:
                if obj.color.image:
                    img = mark_safe(f"""<img src={obj.color.imgs['image']['s']} style='object-fit: contain; object-position: center; border: 1px solid #ededed;'width="24" height=24 />""")
                    return img
                elif obj.color.hex:
                    img = mark_safe(f"""<img style='background-color: {obj.color.hex}; object-fit: contain; object-position: center; border: 1px solid #ededed;' width=24 height=24/>""")
                    return img

                print(obj.color, obj.color.hex, obj.color.image)
               
        return '-'
    color_view.short_description = ""



    readonly_fields = ['image','color_image','color_view']
    fields = ['image','product','name','code','quantity','price','color_image','color','color_view']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    change_list_template = 'admin/change_list.html'
    list_display = [
        'status',
        'order_id',
        'products_cost',
        'created',
        'customer',
        'customer_name',
        'phone',
        'email',
        'coupon',
        'adress',
        'delivery_type',
        'delivery_cost',
    ]
    list_filter = [
        'status',
        'created',
        'delivery_type',
    ]



