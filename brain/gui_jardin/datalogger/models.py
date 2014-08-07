from django.db import models

# Create your models here.
class SoilMoistMesure(models.Model):
   plant = models.CharField(max_length=100)
   time  = models.DateTimeField('Date mesured')
   value = models.IntegerField()
   sec   = models.IntegerField()


   
