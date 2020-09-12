from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class Coupon(admin.ModelAdmin):
    def edit(self,obj): return 'Редактировать'
    readobly_fields = ['edit']
    list_display =  ['edit','discount','unit','minimum','text','expired','once','used']
    list_editable = ['discount','unit','minimum','text','expired','once','used']