from django.conf.urls import patterns, include, url
from core.views import *
from django.contrib import admin
import dhcp.urls


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gui_jardin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^dhcp/', include(dhcp.urls)),
    )
