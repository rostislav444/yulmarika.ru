from django.contrib import admin
from .models import *

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = (
        'time', 'ip', 'user_agent', 'username', 'path', 'result'
    )
    search_fields = ('time','ip','username','path')