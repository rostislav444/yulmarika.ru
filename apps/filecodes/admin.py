from django.contrib import admin
from .models import FileCodes, SocialIcons, YandexKassaAPI, YandexMailAPI, TelegramAPI
from singlemodeladmin import SingleModelAdmin

class SocialIconsInline(admin.TabularInline):
    model = SocialIcons
    extra = 0


@admin.register(FileCodes)
class FileCodesAdmin(SingleModelAdmin):
    inlines = [SocialIconsInline]
    


@admin.register(TelegramAPI)
class TelegramAPIAdmin(SingleModelAdmin):
    pass

@admin.register(YandexKassaAPI)
class YandexKassaAPIAdmin(SingleModelAdmin):
    pass


@admin.register(YandexMailAPI)
class YandexMailAPIAdmin(SingleModelAdmin):
    pass



