# Create your views here
from django.shortcuts import render
from datalogger.models import Plant


def index(request):
    return render(request, "index.pyhtml", {"welcome_string":"Bonjour", "list": Plant.objects.all() })




    
