from django.urls import include, path
from . import views

app_name = 'pages'


urlpatterns = [
    path('<slug>', views.pages, name="page"),

]
