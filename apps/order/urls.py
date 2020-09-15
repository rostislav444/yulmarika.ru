from django.urls import include, path
from django.views.generic import TemplateView
from . import views

app_name = 'order'



urlpatterns = [
    path('cart',               views.order, name="cart"),
    path('decline/<int:order_pk>', views.order_decline, name="decline"),
    path('create/<int:order_pk>',  views.order_create, name="create"),
    path('create',             views.order_create, name="create"),
    path('make_order',         views.make_order, name="make_order"),
    path('order_or_register',  views.order_or_register, name="order_or_register"),
    path('confirmation/<uid>', views.confirmation, name="confirmation"),
    path('success/<int:pk>',   views.order_sucess, name="success"),
    path('success/',           views.order_sucess, name="success"),
    path('yandex_response',    views.yandex_response, name="yandex_response"),
]
