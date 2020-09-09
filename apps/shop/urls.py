from django.urls import include, path, re_path
from . import views

app_name = 'shop'

cart = [
    path('add/',    views.CartViewSet.as_view({'post': 'add'}),    name='cart_add'),
    path('remove/', views.CartViewSet.as_view({'post': 'remove'}), name='cart_remove'),
    path('data/',   views.CartViewSet.as_view({'get': 'data'}),    name='cart_data'),
    path('clear/',  views.CartViewSet.as_view({'get': 'clear'}),   name='cart_clear'),
    path('fast_buy/<product_id>/<variant_id>/', views.CartViewSet.as_view({'get': 'fast_buy'}), name='fast_buy'),
   
]

urlpatterns = [
    re_path(r'^category:(?P<category>[0-9a-zA-Z\&-_]*)/$', views.home, name="home"),
    path('', views.home, name="home"),
    path('product/<slug>/<product_id>/<color>/<variant_id>/', views.product, name="product"),
    path('cart/', include(cart)),
    path('search', views.search, name='search')
]
