# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from site_vostok import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('photos.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]