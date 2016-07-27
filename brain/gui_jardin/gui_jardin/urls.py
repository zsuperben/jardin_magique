from django.conf.urls import patterns, include, url
from core.views import *
from django.contrib import admin
import dhcp.urls
import datalogger.views

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'gui_jardin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', datalogger.views.IndexView),
    url(r'^dhcp/', include(dhcp.urls)),
    ]
