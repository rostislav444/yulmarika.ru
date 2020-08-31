from django.contrib import admin
from .models import BackUpDB

@admin.register(BackUpDB)
class BackUpDBAdmin(admin.ModelAdmin):
    pass