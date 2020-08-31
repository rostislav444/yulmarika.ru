from django.contrib import admin
from .models import *


class PageBlockInline(admin.StackedInline):
    model = PageBlock
    extra = 1

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [PageBlockInline]
