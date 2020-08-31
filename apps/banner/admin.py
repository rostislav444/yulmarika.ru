from django.contrib import admin
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'url', 'image']
    list_editable = ['name', 'description', 'url', 'image']
