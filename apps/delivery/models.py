from django.db import models
from urllib.parse import urlencode
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import JSONField
import requests
from apps.core.function import send_mail


class Delivery(models.Model):
    api_key =   models.CharField(max_length=255, default="", null=True, blank=True, verbose_name="Ключ API")
    api_check = models.CharField(max_length=255, default="", null=True, blank=True, verbose_name="Состояние API ключа")
    response = JSONField(editable=False, null=True, blank=True, default=dict)


    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставка"

    def save(self):
        super(Delivery, self).save()
        self.set_cities()
        super(Delivery, self).save()

    def test_api(self):
        obj = Delivery.objects.all().first()
        data = {'key' : obj.api_key, 'q' : 'getCities'}
        response = obj.send_request(data)
        if type(response) == dict and 'err' in response.keys():
            kwargs = {
                "email" : 'yulmarika@yandex.ru',
                "subject" : "API калькулятора",
                "text" :  response['err'],
            }
            try: send_mail(**kwargs)
            except: pass
        else:
            if type(response) == list:
                for city in response:
                    try:
                        DeliveryCities.objects.get(parent=obj, name=city['name'])
                    except:
                        new_city = DeliveryCities(parent=obj, name=city['name'])
                        new_city.save()
           
        
    def send_request(self, data):
        data['arrivalDoor'] = False
        data['derivalDoor'] = False
        url = '?'.join(['http://api.c6v.ru/', urlencode(data)])
        headers = {"Content-Type": "application/json",}
        response = requests.post(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def set_cities(self):
        data = {'key' : self.api_key, 'q' : 'getCities'}
        try: self.response = self.send_request(data)
        except: pass
        
        if type(self.response) == list:
            self.api_check = 'API работает'
            for city in self.response:
                try:
                    DeliveryCities.objects.get(parent=self, name=city['name'])
                except:
                    new_city = DeliveryCities(parent=self, name=city['name'])
                    new_city.save()

        elif type(self.response) == dict and 'err' in self.response.keys():
            self.api_check = self.response['err']
        else:
            self.api_check = 'Что-то пошло не так'
       

class DeliveryCities(models.Model):
    parent =     models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="cities")
    name =       models.CharField(max_length=255, verbose_name="Название города")
    name_lower = models.CharField(max_length=255, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def save(self):
        self.name_lower = self.name.lower()
        super(DeliveryCities, self).save()
