from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.urls import include, path
import os
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.site.index_template = 'admin/index.html'
admin.site.site_header = 'Администрирование'
admin.site.site_title = 'Администрирование сайта'
admin.site.index_title = 'Администрирование сайта'





urlpatterns = [
    path('',          include('apps.shop.urls')),
    path('order/',    include('apps.order.urls')),
    path('customer/', include('apps.user.urls')),
    path('core/',     include('apps.core.urls')),
    path('coupon/',   include('apps.coupon.urls')),
    path('pages/',    include('apps.pages.urls')),
    path('delivery/', include('apps.delivery.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()