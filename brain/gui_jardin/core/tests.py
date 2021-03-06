"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core import serializers
from core.models import PlantType

class MySimpleTest(TestCase):

    def setUp(self):
        """
        Tries to create objects in the database. 
        """
###     This object creation has moved to "fixtures". 
###     It is evaluated at the same time more or less, and does the same job. 
###     But this data  is also used in production, so to be able to reuse it it 
###     has moved to fixtures.

#        PlantType.objects.create(
#            name="orchid", 
#            mini_soil=1, 
#            maxi_soil=50, 
#            mini_temp=16,
#            maxi_temp=40,
#            light_growth=43200,
#            light_g_intensity=512,
#            light_bloom=43200,
#            light_b_intensity=384,
#            growth_time=15552000,
#            harvest_stress=False,
#            additional_requirements=True,
#
#            )
#        PlantType.objects.create(
#            name="tomate", 
#            mini_soil=50, 
#            maxi_soil=400, 
#            mini_temp=12,
#            maxi_temp=32,
#            light_growth=16*3600,
#            light_g_intensity=768,
#            light_bloom=12*3600,
#            light_b_intensity=768,
#            growth_time=24*3600*7*5,
#            harvest_stress=True,
#            hstress_length=24*3600*7,
#            additional_requirements=False,
#            )
#
    def test_print_serialized_data(self):
        print(serializers.serialize('xml', PlantType.objects.all()))

