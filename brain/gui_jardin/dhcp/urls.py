from django.conf.urls import url 
from dhcp.views import *

urlpatterns = [
url(r'^dhcp/form/$', CreateConfigView.get),
]
