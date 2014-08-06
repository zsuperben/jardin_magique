from django.db import models

# Create your models here.
class SoilMoistMesure(models.Model):
   plant = models.CharField(max_length=100)
   date  = models.DateTimeField('Date mesured')
   value = models.IntegerField()
