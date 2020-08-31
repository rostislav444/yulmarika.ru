from django.urls import path
from . import views 

app_name = 'delivery'

urlpatterns = [
    path('save_adress',  views.UserAdressViewSet.as_view({'post' : 'save_adress'}), name="save_adress"),
    path('get_adress',   views.UserAdressViewSet.as_view({'get' :  'get_adress'}),  name="get_adress"),
    path('set_adress',   views.UserAdressViewSet.as_view({'post' : 'set_adress'}),  name="set_adress"),
]