from django.test import TestCase
from django.core import serializers
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

        b = PlantType.objects.get(name = 'orchid')
        Plant.objects.create(
            espece = b,
            name = 'berte',
            )
        Plant.objects.create(
            espece = PlantType.objects.get(name="tomate"),
            name = 'toto',
            )

    def test_create_Plants_1(self):

        b = PlantType.objects.get(name = 'orchid')
        Plant.objects.create(
            espece = b,
            name = 'berte',
            )


    def test_2(self):            
            Plant.objects.create(
                espece = PlantType.objects.get(name = 'tomate'),
                )

        
    def test_create_SoilMoistMesure(self):
        SoilMoistMesure.objects.create(
            time = timezone.now(),
            value = 1024,
            plant = Plant.objects.get(name = 'berte'),
            )
        SoilMoistMesure.objects.create(
            time = timezone.now(),
            plant = Plant.objects.get(name = 'toto'),
            value = 512,
            )


    def test_method_get(self):
        c = PlantType.objects.get(name__exact='orchid')
        self.assertEqual(c.has_plant(), True)
    def test_isok(self):
        f = SoilMoistMesure.objects.create(
            time = timezone.now(),
            value = 1024,
            plant = Plant.objects.get(name = 'toto'),
            )

        self.assertEqual(f.is_OK(), False)

    def test_print_serialized_objects(self):
        print(serializers.serialize('xml', PlantType.objects.all()))
        print("\n %s" % serializers.serialize('xml', Plant.objects.all()))
