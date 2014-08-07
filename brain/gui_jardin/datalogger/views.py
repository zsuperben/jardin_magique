from django.shortcuts import render
from djanggo.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django import forms


# Create your views here.
def record_mesure(request):
    if request.method == 'POST' && "plant", "time", "value", "sec" in request.POST:
        if request.POST["time"] * request.POST["value"] % 13 == request.POST["sec"]:
            # Process data and save it to db. 
            SoilMoistMesure.create(request.POST) # il faut ajouter le traitement des erreurs 

        
