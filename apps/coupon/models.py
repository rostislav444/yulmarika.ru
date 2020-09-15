from django.db import models


class Coupon(models.Model):
    units = (
        ('percent','Проценты'),
        ('rub', 'Рубли'),
    )
    discount = models.PositiveIntegerField(blank=False, null=False, verbose_name="Сумма скидки")
    unit =     models.CharField(choices=units, blank=False, null=False, max_length=255, verbose_name="Измерение")
    minimum =  models.PositiveIntegerField(blank=False, null=False, verbose_name="Минимальная сумма заказа")
    text =     models.CharField(blank=False, null=False, max_length=1000, verbose_name="Текст промокода")
    expired =  models.BooleanField(default=False, verbose_name="Срок действия закончился")
    once =    models.BooleanField(default=False, verbose_name="Использовать только 1 раз")
    used =     models.BooleanField(default=False, verbose_name="Использован")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"