from django.urls import include, path
from django.views.generic import TemplateView
from . import views

app_name = 'order'



urlpatterns = [
    path('cart', TemplateView.as_view(template_name="shop/order/order.html"), name="cart"),
    path('payment', views.payment, name="payment"),
    path('create', views.order_create, name="create"),
    path('make_order', views.make_order, name="make_order"),
    path('order_or_register', views.order_or_register, name="order_or_register"),
   
]
