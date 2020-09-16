from django.db import models
from django.utils import timezone
from apps.coupon.models import Coupon
from apps.core.function import send_mail
from collections import OrderedDict
from apps.filecodes.models import FileCodes, TelegramAPI
from django.contrib.postgres.fields import JSONField
import urllib.request
import urllib.parse

class Order(models.Model):
    ORDER_STATUS = [
        ('new',        'Новый заказ'),
        ('created',    'Создан, ожидает оплаты'),
        ('payed',      'Оплачен, в обработке'),
        ('prepered',   'Собран, ожидает передачи на доставку'),
        ('at_delivry', 'Передан на доставку'),
        ('delivring',  'Доставляется'),
        ('delivred',   'Доставлен'),
        ('declined',   'Отменен'),
    ]
    status_old =    models.CharField(max_length=255, editable=False, blank=True, null=True, choices=ORDER_STATUS, verbose_name="Статус заказа")
    status =        models.CharField(max_length=255, choices=ORDER_STATUS, verbose_name="Статус заказа")
    order_id =      models.PositiveIntegerField(unique=True, verbose_name="Номер заказа")
    products_cost = models.PositiveIntegerField(blank=True, default=0, verbose_name="Стоимость товаров")
    discount_cost = models.PositiveIntegerField(blank=True, default=0, verbose_name="Скидка по купону")
    delivery_cost = models.PositiveIntegerField(blank=True, default=0, verbose_name="Стоимость доставки")
    free_delivery = models.BooleanField(default=False, verbose_name="Бесплатная доставка")
    created =       models.DateTimeField(blank=True, null=True, verbose_name="Время заказа", default=timezone.now)
    payed =         models.DateTimeField(blank=True, null=True, verbose_name="Время оплаты", default=None)
    customer =      models.ForeignKey('user.CustomUser', on_delete=models.SET_NULL, editable=True, blank=True, null=True, verbose_name="Покупатель", related_name="orders")
    customer_name = models.CharField(max_length=500, verbose_name="Покупатель")
    phone =         models.CharField(max_length=24, verbose_name="Телефон")
    email =         models.EmailField(max_length=50, blank=True, null=True, verbose_name="Email")
    coupon =        models.ForeignKey(Coupon, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Скидочный купон")
    adress =        models.TextField(verbose_name="Адрес доставки")
    comments =      models.TextField(verbose_name="Примечания к заказу", blank=True, null=True)
    delivery_type =  models.CharField(max_length=24, verbose_name="Способ доставки")
    track_number_old = models.CharField(max_length=500, default="", unique=False, editable=False, blank=True)
    track_number =     models.CharField(max_length=500, default="", unique=False, blank=True, verbose_name="Трэк-номер")
    uid =          models.CharField(max_length=500, unique=False, default='', null=True, blank=True, verbose_name="UUID")
    weight =        models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Вес коробки")
    width  =        models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Ширина коробки")
    height  =       models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Высота коробки")
    length  =       models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Длина коробки")
    

    class Meta:
        ordering = ['-created']
        verbose_name = "Список заказов"
        verbose_name_plural = "Список заказов"

    def __str__(self):
        return ' - '.join(['status','order_id','products_cost'])

    @property
    def initial_cost(self):
        return int(self.products_cost) + int(self.discount_cost)

    @property
    def order_satus(self):
        return dict(self.__class__.ORDER_STATUS).get(self.status)

    def telegram_msg(self):
        api = TelegramAPI.objects.first()
        if api and api.chanel_id and api.api_key:
            chanel_id = api.chanel_id
            api_key =   api.api_key
        else:
            chanel_id = "1270278191"
            api_key = "1130353501:AAHQWTGljZtT39hv5cohgQ8scmp42BFp7GU"

        if self.status == 'payed':
            msg = f"Заказ №{self.order_id}\n\n"

            for n, item in enumerate(self.products.all()):
                name = item.product.name
                code = item.product.code
                price = str(item.product.price)
                variant = item.variant
                color = item.color.name
                qty = str(item.quantity)

                msg += f"{n+1}. {code} - {name}\nцвет: {color} \n{qty} шт. x {price} RUB\n"

            msg += f"\nСтоимость товаров: {str(self.products_cost)}\n"
            msg += f"Размер скидки: {str(self.discount_cost)}\n"
            msg += f"Клиент: {str(self.customer_name)}\n"
            msg += f"Способ доставки: {str(self.delivery_type)}\n"
            msg += f"Стоимость доставки: {str(self.delivery_cost)} RUB\n"
            msg += f"Телфон: {str(self.phone)}\n"
            msg += f"Адрес: {str(self.adress)}\n"
            msg += f"Комментарий: {str(self.comments)}\n"
            
            try:
                msg = urllib.parse.quote(msg)
                url = f"https://api.telegram.org/bot{api_key}/sendMessage?chat_id=-100{chanel_id}&text=" + msg
                contents = urllib.request.urlopen(url).read()
            except: pass

    def save(self):
        fk = FileCodes.objects.first()
        if fk:
            if self.products_cost >= fk.free_delivery:
                self.free_delivery = True
        
        # Set track number event
        if self.track_number_old != self.track_number:
            kwargs = {
                "email" :  self.email,
                "subject" : f"Трек номер заказа: {self.track_number}",
                "text" :    f"Для отправления с Вашим заказом установлен трек-номер '{self.track_number}', по которому Вы можете отслеживать перемещения Вашего заказа из магазина Юлмарика",
            }
            try: send_mail(**kwargs)
            except: pass
            self.track_number_old = self.track_number
        
        # Set old as declined
        if self.customer:
            self.customer.orders.filter(status__in=['new','created']).exclude(pk=self.pk).update(status='declined')
    
        if self.status_old != self.status and self.email:
            status = OrderedDict(self.ORDER_STATUS)[self.status] 
            if self.status == 'created':
                kwargs = {
                    "email" :   self.email,
                    "subject" : "Заказ: Создан, ожидает оплаты",
                    "text" :    "Заказ в магазине Юлмарика создан. Пожалуйста, не забудьте его оплатить",
                }
            elif self.status == 'payed':
                # FOR ADMIN
                self.telegram_msg()
                # FOR USER
                kwargs = {
                    "email" :   self.email,
                    "subject" : "Заказ: Успешно оплачен!",
                    "text" :   f"Ваш заказ {self.order_id} в магазине Юлмарика успешно оплачен. Мы будем информировать вас об отправлении вашего заказа и изменениях статуса его доставки. Благодарим Вас за покупку в нашем магазине!",
                }
            elif self.status == 'prepered':
                kwargs = {
                    "email" :   self.email,
                    "subject" : "Заказ: Собран, ожидает передачи на доставку",
                    "text" :    "Ваш заказ в магазине Юлмарика собран и ожидает передачи службе доставки.",
                }
            elif self.status == 'at_delivry':
                kwargs = {
                    "email" :  self.email,
                    "subject" : "Заказ: Передан на доставку",
                    "text" :    "Ваш заказ в магазине Юлмарика передан службе доставки. Совсем скоро он будет у вас.",
                }
            elif self.status == 'delivring':
                kwargs = {
                    "email" :   self.email,
                    "subject" : "Заказ: Доставляется",
                    "text" :    "Ваш заказ в магазине Юлмарика уже в пути. Служба доставки везёт его к Вам.",
                }
            elif self.status == 'delivred':
                kwargs = {
                    "email" :   self.email,
                    "subject" : "Заказ: Доставлен",
                    "text" :    "По информации от службы доставки, Ваш заказ в магазине Юлмарика был Вам доставлен. Надеемся, что Вы остались довольны от сотрудничества с Юлмарика и порекомендуете наш магазин своим друзьям.",
                }
            elif self.status in ['new','declined']:
                pass
            else:
                kwargs = {
                    "email" :  self.email,
                    "subject" : f"Статус Вашего заказа: {status}",
                    "text" :    f"Статус Вашего заказа, был изменен на {status}",
                }

            try: send_mail(**kwargs)
            except: pass



        self.status_old = self.status
        if not self.pk:
            last_order = Order.objects.all().order_by('order_id').last()
            self.order_id = last_order.order_id + 1 if last_order else 1
        super(Order, self).save()




class OrderProduct(models.Model):
    parent =   models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")
    product =  models.ForeignKey('shop.Product', on_delete=models.CASCADE, blank=True, null=True, related_name="orders", verbose_name="Продукт")
    variant =  models.ForeignKey('shop.Variant', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Вариант")
    name =     models.CharField(max_length=255, verbose_name="Название")
    code =     models.CharField(max_length=255, verbose_name="Артикул")
    quantity = models.PositiveIntegerField(verbose_name="Количесвто, шт", default=1, blank=False)
    price =    models.PositiveIntegerField(verbose_name="Цена за шт", null=True, blank=True)
    color =    models.ForeignKey('shop.Color', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Цвет")

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    
    @property
    def total(self):
        return int(self.price) * int(self.quantity)

    def save(self):
        if not self.pk and self.product:
            self.name, self.price, self.code = self.product.name, self.product.price, self.product.code
        super(OrderProduct, self).save()


class YandexResponse(models.Model):
    time =  models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Дата создания")
    data =  JSONField(editable=True, null=True, blank=True, default=dict)

    def __str__(self):
        return str(self.time)