from django.db import models
import socket
from core.models import Plant

# Create your models here.
class Sensor(models.Model):
    """
    This model is used to keep track of the configured sensors in the system
    """
    mac        = models.CharField(max_length=12)
    ip         = models.GenericIPAddressField()
    
    pinA0      = models.ForeignKey(Plant, related_name="PinA0")
    pinA0.blank = True
    pinA0.null = True

    pinA1      = models.ForeignKey(Plant, related_name="PinA1")
    pinA1.blank = True
    pinA1.null = True
    
    pinA2      = models.ForeignKey(Plant, related_name="PinA2")
    pinA2.blank = True
    pinA2.null = True
    
    pinA3      = models.ForeignKey(Plant, related_name="PinA3")
    pinA3.blank = True
    pinA3.null = True
    
    pinA4      = models.ForeignKey(Plant, related_name="PinA4")
    pinA4.blank = True
    pinA4.null = True

    pinA5      = models.ForeignKey(Plant, related_name="PinA5")
    pinA5.blank = True
    pinA5.null = True

    name       = models.CharField(max_length=50)
    name.blank = True
    name.null  = True
    
    def __unicode__(self):
        if name is not "":
            return unicode(name)
        else:
            return unicode(mac)


    def __str__(self):
        return str(self.__unicode__())

    def __ip_to_str__(self):
        a = []
#        return socket.inet_ntoa(hex(self.ip)[2:].zfill(8).decode(hex)


class Config(models.Model):
    
    name               = models.CharField(max_length=40)
    logfacility        = models.CharField(max_length=30)
    domain             = models.CharField(max_length=100)
    default_lease_time = models.IntegerField()
    max_lease_time     = models.IntegerField()
    running            = models.BooleanField()



class Rpi(models.Model):
    
    ip                 = models.GenericIPAddressField()
    name               = models.CharField(max_length=50)

class Netboot(models.Model):
    
    server             = models.GenericIPAddressField()
    filename           = models.CharField(max_length=50)

class Networks(models.Model):

    netaddr            = models.GenericIPAddressField()
    netmask            = models.GenericIPAddressField()
    
    startip            = models.GenericIPAddressField()
    startip.null       =True
    startip.blank      =True

    endip              = models.GenericIPAddressField()
    endip.null         = True
    endip.blank        = True

    netboot            = models.ForeignKey(Netboot)
    netboot.blank      = True
    netboot.null       = True

    gateway            = models.GenericIPAddressField()
    gateway.blank      = True
    gateway.null       = True
    
    config             = models.ForeignKey(Config)

