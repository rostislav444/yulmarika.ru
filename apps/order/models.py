from django.db import models
from django.utils import timezone
from apps.coupon.models import Coupon
from apps.core.function import send_mail
from collections import OrderedDict

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
    created =       models.DateTimeField(blank=True, null=True, verbose_name="Время заказа", default=timezone.now)
    payed =         models.DateTimeField(blank=True, null=True, verbose_name="Время оплыта", default=timezone.now)
    customer =      models.ForeignKey('user.CustomUser', on_delete=models.SET_NULL, editable=False, blank=True, null=True, verbose_name="Покупатель", related_name="orders")
    customer_name = models.CharField(max_length=500, verbose_name="Покупатель")
    phone =         models.CharField(max_length=24, verbose_name="Телефон")
    email =         models.EmailField(max_length=50, blank=True, null=True, verbose_name="Email")
    coupon =        models.ForeignKey(Coupon, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Скидочный купон")
    adress =        models.TextField(verbose_name="Адрес доставки")
    comments =      models.TextField(verbose_name="Примечания к заказу", blank=True, null=True)
    delivery_type =  models.CharField(max_length=24, verbose_name="Способ доставки")
    track_number =  models.CharField(max_length=500, unique=True, null=True, blank=True, verbose_name="Трэк-номер")

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

    

    def save(self):
        if self.customer:
            self.customer.orders.filter(status__in=['new','created']).update(status='declined')
               


        if self.status_old != self.status and self.email:
            status = OrderedDict(self.ORDER_STATUS)[self.status] 
            kwargs = {
                "email" : self.email,
                "subject" : f"Статус Вашего заказа: {status}",
                "text" : f"Статус Вашего заказа, был изменен на {status}",
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
    product =  models.ForeignKey('shop.Product', on_delete=models.CASCADE, blank=True, null=True, related_name="orders")
    name =     models.CharField(max_length=255, verbose_name="Название")
    code =     models.CharField(max_length=255, verbose_name="Артикул")
    quantity = models.PositiveIntegerField(verbose_name="Количесвто, шт", default=1, blank=False)
    price =    models.PositiveIntegerField(verbose_name="Цена за шт", null=True, blank=True)
    color =    models.ForeignKey('shop.Variant', on_delete=models.SET_NULL, blank=True, null=True)

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


