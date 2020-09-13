from django.db import models
from django.utils import timezone


class LoginLog(models.Model):
    time =       models.DateTimeField(default=timezone.now, verbose_name="Время попытки входа")
    ip =         models.CharField(blank=True, null=True, max_length=255, verbose_name="IP адрес")
    user_agent = models.CharField(blank=True, null=True, max_length=500, verbose_name="Юзер-агент")
    username =   models.CharField(blank=True, null=True, max_length=255, verbose_name="Логин")
    path =       models.CharField(blank=True, null=True, max_length=500, verbose_name="Адрес авторизации")
    result =     models.BooleanField(default=False)

    class Meta:
        verbose_name = "Авторизация в системе"
        verbose_name_plural = "Авторизации в системе"


    def get_client_ip(self, request):
        print(request.META.get('HTTP_USER_AGENT'))
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for: ip = x_forwarded_for.split(',')[0]
        else: ip = request.META.get('REMOTE_ADDR')
        return ip

    def set_request_data(self, request):
        headers = request.headers
        login_kwargs = {
            'user_agent' : headers.get('User-Agent'),
            'path' : headers['Referer'] if 'Referer' in  headers else None,
            'ip' : self.get_client_ip(request),
        }
        for key, value in login_kwargs.items():
            setattr(self, key, value)
        return self 

    def save(self, request=None):
        if request:
            self = self.set_request_data(request)
        super(LoginLog, self).save() 