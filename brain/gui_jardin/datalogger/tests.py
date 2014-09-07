from django.test import TestCase
from datalogger.models import *
from core.tests import *
from django.utils import timezone 

# Create your tests here.

# Tries to create objects in the database. 

class CreateObjects(TestCase):
    """
    Tries to create object in the database from models. 
    """
    def setUp(self):
        PlantType.objects.create(
            name="orchid", 
            mini_soil=1, 
            maxi_soil=50, 
            mini_temp=16,
            maxi_temp=40,
            light_growth=43200,
            light_g_intensity=512,
            light_bloom=43200,
            light_b_intensity=384,
            growth_time=15552000,
            harvest_stress=False,
            additional_requirements=True,

            )
        PlantType.objects.create(
            name="tomate", 
            mini_soil=50, 
            maxi_soil=400, 
            mini_temp=12,
            maxi_temp=32,
            light_growth=16*3600,
            light_g_intensity=768,
            light_bloom=12*3600,
            light_b_intensity=768,
            growth_time=24*3600*7*5,
            harvest_stress=True,
            hstress_length=24*3600*7,
            additional_requirements=False,
            )
    def test_create_Plants_1(self):

            b = PlantType.objects.get(name = 'orchid')
            Plant.objects.create(
                espece = b,
                position = 1, 
                name = 'berte',
                )


    def test_2(self):            
            Plant.objects.create(
                espece = PlantType.objects.get(name = 'tomate'),
                position = 2, 
                )

        
    def test_create_SoilMoistMesure(self):
        SoilMoistMesure.objects.create(
            time = timezone.now(),
            value = 1024,
            plant = Plant(0),
            )
        SoilMoistMesure.objects.create(
            time = timezone.now(),
            plant = Plant(1),
            value = 512,
            )


    def test_method_get(self):
        c = PlantType.objects.get(name = 'orchid')
        self.assertEqual(c.has_plant(), True)
