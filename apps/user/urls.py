from django.urls import include, path
from django.views.generic import TemplateView
from . import views

app_name = 'user'

profile = [
    path('orders',  views.UserProfile.as_view({'get':'orders'}),             name="profile_orders"),
    path('data',    views.UserProfile.as_view({'get':'data','post':'data'}), name="profile_data"),
    path('adress',  views.UserProfile.as_view({'get':'adresses','post':'adresses'}),           name="profile_adresses"),
    path('exit',    views.UserProfile.as_view({'get':'exit'}),               name="profile_exit"),
]

urlpatterns = [
    path('auth_register_or_order', TemplateView.as_view(template_name="user/auth_register_or_order.html"), name="auth_register_or_order"),
    path('login',                  TemplateView.as_view(template_name="user/auth_or_reister.html"),        name="login"),
    path('auth',      views.UserViewSet.as_view({'post': 'auth'}),     name="auth"),
    path('register',  views.UserViewSet.as_view({'post': 'register'}), name="register"),
    path('profile/',  include(profile))
]
