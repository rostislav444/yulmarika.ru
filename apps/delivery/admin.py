from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Delivery, DeliveryCities

class DeliveryCitiesInline(admin.StackedInline):
    model = DeliveryCities
    extra = 0

@admin.register(Delivery)
class DeliveryAdmin(SingleModelAdmin):
    inlines = []
    readonly_fields = ['api_check']
    fileds = ['api_check','api_key']
    