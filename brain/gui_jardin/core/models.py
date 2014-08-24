from django.db import models
from datalogger.models import Plant
# Create your models here.
class PlantType(models.Model):

    name            = models.TextField(max_length=50)
    name.db_index   = True
    mini_soil       = models.IntegerField()
    maxi_soil       = models.IntegerField()
    mini_temp       = models.IntegerField()
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

     
    
     


    def has_plant(self):

        try: 
            if self.name in datalogger.Plant:
                return True

            else:
                return False

        except:
            print("you no can code, broken language")
            
