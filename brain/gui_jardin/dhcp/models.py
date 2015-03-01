from django.db import models
import socket
from core.models import Plant

# Create your models here.
class Sensor(models.Model):
    """
    This model is used to keep track of the configured sensors in the system
    """
    mac        = models.CharField(max_length=12)
    ip         = models.IPAddressField()
    
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
    
    logfacility        = models.CharField(max_length=30)
    domain             = models.CharField(max_length=100)
    default_lease_time = models.IntegerField()
    max_lease_time     = models.IntegerField()


class Rpi(models.Model):

    ip                 = models.IPAddressField()
    name               = models.CharField(max_length=50)

class Netboot(models.Model):
    server             = models.IPAddressField()
    filename           = models.CharField(max_length=50)

class Networks(models.Model):

    netaddr            = models.IPAddressField()
    netmask            = models.IPAddressField()
    
    startip            = models.IPAddressField()
    startip.null       =True
    startip.blank      =True

    endip              = models.IPAddressField()
    endip.null         = True
    endip.blank        = True

    netboot            = models.OneToOneField(Netboot)
    netboot.blank      = True
    netboot.null       = True

    gateway            = models.IPAddressField()
    gateway.blank      = True
    gateway.null       = True
    
    config             = models.ForeignKey(Config)

