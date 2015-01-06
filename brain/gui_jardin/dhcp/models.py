from django.db import models

# Create your models here.
class KnownSensor(Model):
    """
    This model is used to keep track of the configured sensors in the system
    """
    mac        = models.CharField(max_length=12)
    
    
    name       = models.CharField(mac_length=50)
    name.blank = True
    name.null  = True
    
    def __unicode__(self):
        if name is not "":
            return unicode(name)
        else:
            return unicode(mac)


    def __str__(self):
        return str(self.__unicode__())



