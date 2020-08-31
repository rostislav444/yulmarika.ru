from django.urls import include, path
from . import views

app_name = 'core'

search = [
    path('city', views.SearchViewSet.as_view({'post': 'city'}), name="search_city")
]

urlpatterns = [
    path('search/', include(search))
]
