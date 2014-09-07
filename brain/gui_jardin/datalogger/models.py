from django.db import models


class Plant(models.Model):
    
    espece   = models.ForeignKey('core.PlantType') 
    position = models.IntegerField()
    name     = models.CharField(max_length=50)
    name.blank = True
    name.null  = True
# Create your models here.
class SoilMoistMesure(models.Model):
   plant      = models.ForeignKey('Plant')
   time       = models.DateTimeField('Date mesured')
   value      = models.IntegerField()

   def is_OK(self):
      if plant_type.mini_soil < value < plant_type.maxi_soil:
         return True
      else:
         return False



class TempHumMesure(models.Model):
   time = models.DateTimeField('Date mesured')
   temp = models.IntegerField()
   humi = models.IntegerField()



   def is_too_hot(self):
      if temp > 40:
         return True
      else:
         return False

   def is_to_cold(self):
      if temp < 10:
         return True
      else:
         return False


   def is_OK(self):
      if not self.is_too_hot() and not self.is_too_cold():
         return True

      else:
         return False


