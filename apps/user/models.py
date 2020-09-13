from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils import timezone
import datetime
import jsonfield

VERBOSE_NAME = 'Appname'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, admin=False, data={}):
        if not email:
            raise ValueError('Пользователь должен иметь адрес элетронной почты')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, admin=True)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    GENDER = [
        ('male', 'М'),
        ('female', 'Ж'),
    ]

    user_id =       models.PositiveIntegerField(unique=True, verbose_name="ID пользователя")
    gender =        models.CharField(max_length=6, choices=GENDER, verbose_name="Пол")
    name =          models.CharField(max_length=50, verbose_name="Имя")
    surname =       models.CharField(max_length=50, verbose_name="Фамилия")
    phone =         models.CharField(max_length=16, verbose_name="Номер телефона")
    phone_checked = models.BooleanField(default=False, verbose_name="Номер телефона подтвержден")
    email =         models.EmailField(max_length=255, unique=True, verbose_name="Электронная почта")
    email_checked = models.BooleanField(default=False, verbose_name="Электронная почта подтверждена")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    password =      models.CharField(max_length=500, verbose_name="Пароль")
    city =          models.CharField(max_length=255, verbose_name="Город")
    street =        models.CharField(max_length=255, verbose_name="Улица")
    house =         models.CharField(max_length=255, verbose_name="Номер дома")
    appartment =    models.CharField(max_length=255, verbose_name="Номер квартиры")
    index =         models.CharField(max_length=255, verbose_name="Почтовый индекс")
    add_info =      models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")
    created =       models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Дата создания")
    updated =       models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Последнее изменение")
    birthday =      models.DateField(default=timezone.now, blank=True, null=True, verbose_name="Дата рожденья")
    is_active = models.BooleanField(default=True)
    is_admin =  models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-created']
        verbose_name = "Аккаунт Пользователя"
        verbose_name_plural = "Аккаунты Пользователей"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def user_order(self):
        return self.orders.exclude(status='new')


    def save(self,*args,**kwargs):
        # Time 
        if not self.pk:
            last_user = CustomUser.objects.all().order_by('user_id').last()
            self.user_id = last_user.user_id + 1 if last_user else 1
        self.updated = timezone.now()
        super(CustomUser, self).save(*args,**kwargs)


class UserAdress(models.Model):
    user =       models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="adress")
    name     =   models.CharField(max_length=50,  blank=True, null=True, verbose_name="Имя")
    surname  =   models.CharField(max_length=50,  blank=True, null=True, verbose_name="Фамилия")
    phone  =     models.CharField(max_length=50,  blank=True, null=True, verbose_name="Телефон")
    city  =      models.CharField(max_length=50,  blank=True, null=True, verbose_name="Город")
    street  =    models.CharField(max_length=50,  blank=True, null=True, verbose_name="Улица")
    house  =     models.CharField(max_length=50,  blank=True, null=True, verbose_name="Дом")
    apartment  = models.CharField(max_length=50,  blank=True, null=True, verbose_name="Квартира / офис")
    add_info  =  models.CharField(max_length=250, blank=True, null=True, verbose_name="Дополнительная информация")
    selected =   models.BooleanField(default=False)
    delivery =   jsonfield.JSONField(editable=True, null=True, blank=True, default='{}')

    class Meta:
        ordering = ['-selected','pk']

    