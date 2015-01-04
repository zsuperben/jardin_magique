from django.db import models
from core.models import  Plant


class SoilMoistMesure(models.Model):
   plant      = models.ForeignKey(Plant)
   time       = models.DateTimeField('Date and time of the mesure')
   value      = models.IntegerField()

   def is_OK(self):
      p = self.plant
      print(p) 
      e = p.espece
      print(e)
      if e.mini_soil < self.value < e.maxi_soil:
         return True
      else:
         return False



class TempHumMesure(models.Model):
   time = models.DateTimeField('Date and time of the mesure')
   temp = models.IntegerField()
   humi = models.IntegerField()
   plant = models.ForeignKey(Plant)



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


