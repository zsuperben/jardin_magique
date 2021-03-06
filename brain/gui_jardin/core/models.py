from django.db import models
#from dhcp.models import Sensor
# Create your models here.


class PlantType(models.Model):
    """
    This model tries to describe in a first sketch what are the variables we need to account to grow plants of all sorts. 
    """
    # Name with index in database to speed up research 
    name            = models.CharField(max_length=50)




    # soil humidity 
    mini_soil       = models.IntegerField()
    maxi_soil       = models.IntegerField()
    
    
    
    
    # Temperatures section
    mini_temp       = models.IntegerField()
    mini_temp_night = models.IntegerField()
    mini_temp_night.null  = True
    mini_temp_night.blank = True
    

    maxi_temp       = models.IntegerField()
    light_growth    = models.IntegerField()
    light_g_intensity = models.IntegerField()
    light_bloom     = models.IntegerField()
    light_b_intensity = models.IntegerField()
    growth_time     = models.IntegerField()
    
    harvest_stress  = models.BooleanField()
    hstress_length  = models.IntegerField()
    hstress_length.null  = True
    hstress_length.blank = True
    
    additional_requirements = models.BooleanField()
    additional_table = models.CharField(max_length=50)
    additional_table.null = True 
    additional_table.blank = True 
     
    
    def __unicode__(self):
        return unicode(self.name)


    def has_plant(self):
        from datalogger.models import Plant
        try: 
            q = Plant.objects.filter(espece = self)
            if len(q) > 0:
                return True

            else:
                return False

        except:
            print("you no can code, broken language")
 
 
class Plant(models.Model):
        
    espece   = models.ForeignKey(PlantType) 
    position = models.CharField(max_length=10)
    name     = models.CharField(max_length=50)
#    sensor   = models.ForeignKey(Sensor)
    def __unicode__(self):
        retval = "position : %s, espece : %s" % (str(self.id), str(self.espece.name))
        if self.name is not None:
            retval = retval + ", name : %s" % self.name
        return unicode(retval)

    def __str__(self):
        return str(self.__unicode__())

           
