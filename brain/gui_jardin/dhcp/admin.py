from django.contrib import admin
from dhcp.models import *

admin.site.register(Sensor)
admin.site.register(Config)
admin.site.register(Rpi)
admin.site.register(Netboot)
admin.site.register(Networks)


