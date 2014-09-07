"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from core.models import PlantType
#from core import models

class MySimpleTest(TestCase):

    def test_create_PlantType(self):
        """
        Tries to create objects in the database. 
        """
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
