from django.contrib import admin
from .models import FileCodes, SocialIcons
from singlemodeladmin import SingleModelAdmin

class SocialIconsInline(admin.TabularInline):
    model = SocialIcons
    extra = 0


@admin.register(FileCodes)
class FileCodesAdmin(SingleModelAdmin):
    inlines = [SocialIconsInline]