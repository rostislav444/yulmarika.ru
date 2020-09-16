from django.contrib import admin
from django.utils.html import mark_safe
from project import settings
import json
from .models import (
    Category, Color, WhoIntended, GiftReason, ProductStatus, Product, Variant,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def edit(self, obj=None):
        return 'Редактировать'
    
    readonly_fields = ['edit']
    list_display =  ['edit','name','in_catalogue','in_recomendation']
    fields =        ['name','in_catalogue','in_recomendation']
    list_editable = ['name','in_catalogue','in_recomendation']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    def color_view(self, obj=None):
        if obj.pk:
            if obj.image:
                img = mark_safe(f"""<img src={obj.imgs['image']['s']} style='object-fit: contain; object-position: center; border: 1px solid #ededed;'width="24" height=24 />""")
                return img
            elif obj.hex:
                img = mark_safe(f"""<img style='background-color: {obj.hex}; object-fit: contain; object-position: center; border: 1px solid #ededed;' width=24 height=24/>""")
                return img

        return '-'
    color_view.short_description = "Цвет"

    def products(self, obj):
        if obj.pk:
            return len(obj.variants.all())
        return 0

    products.short_description = "Товаров"
    
    readonly_fileds = ['color_view','products']
    list_display = ['color_view','name','products']
    list_display_links = ('color_view','name')

@admin.register(WhoIntended)
class WhoIntendedAdmin(admin.ModelAdmin):
    pass

@admin.register(GiftReason)
class GiftReasonAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductStatus)
class ProductStatusAdmin(admin.ModelAdmin):
    pass

def imgView(self, fieldname, obj=None):
    if obj:
        if getattr(obj, fieldname).name:
            thmbs = getattr(obj, fieldname + '_thmb')
            
            if thmbs is not None and type(thmbs) is not dict:
                thmbs = json.loads(thmbs)
         
            # if 'main' in thmbs.keys():
            #     url =  settings.MEDIA_URL + thmbs.get('main')
            #     img = mark_safe("""<img style="object-fit: cover; object-position: center; border: 1px solid #ededed;" 
            #     src="{url}" width="{width}" height={height} />""".format(url=url, height=120, width=120))
            #     return img
            if 's' in thmbs.keys():
                url =  settings.MEDIA_URL + thmbs.get('s')
                img = mark_safe("""<img style="object-fit: cover; object-position: center; border: 1px solid #ededed;" 
                src="{url}" width="{width}" height={height} />""".format(url=url, height=120, width=90))
                return img
           
    return '-'




class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0
    # Product card
    def photo_1_view(self, obj=None): return imgView(self, 'photo_1', obj)
    photo_1_view.short_description = ""
    def photo_2_view(self, obj=None): return imgView(self, 'photo_2', obj)
    photo_2_view.short_description = ""
    def photo_3_view(self, obj=None): return imgView(self, 'photo_3', obj)
    photo_3_view.short_description = ""
    def photo_4_view(self, obj=None): return imgView(self, 'photo_4', obj)
    photo_4_view.short_description = ""

    readonly_fields = ['photo_1_view','photo_2_view','photo_3_view','photo_4_view']
    fields = [
       'first','color',
        ('photo_1','photo_1_view',),
        ('photo_2','photo_2_view',),
        ('photo_3','photo_3_view',),
        ('photo_4','photo_4_view',),
        'in_stock','hide'
    ]

   


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_form_template = 'admin/custom_change_form.html'
    change_list_template = 'admin/change_list.html'

    # If product have variant
    def product_card(self, obj=None): return imgView(self, 'image', obj)
    product_card.short_description = 'Карточка товара'
    
    # Product card
    def image_view(self, obj=None): return imgView(self, 'image', obj)
    image_view.short_description = ""

    # Add image card 
    def add_image_view(self, obj=None): 
        return imgView(self, 'add_image', obj)
    add_image_view.short_description = ""

    readonly_fields = ['image_view','add_image_view']
    fields = [
        'meta_title','meta_descr',
        'name','code','price','old_price','category','who_intended','gift_reason','status',
        'in_sell','is_popular',
        ('image','image_view','image_thmb',),('add_image','add_image_view',),
        'length','width','height','weight',
        'description','preferences',
        'created','updated'
    ]

    search_fields = ['name','code']
    list_display = ['name','code','price','created','in_sell','is_popular','product_card']
    list_display_links = ('name', 'product_card',)
    inlines = [VariantInline]





