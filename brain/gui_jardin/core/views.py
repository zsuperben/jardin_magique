# Create your views here
from django.shortcuts import render
from datalogger.models import Plant


def index(request):

    if  Plant.objects.all() == []:
        return render(request, "index_no_plants.pyhtml", { "welcome_string":"Hey!", "sorry_string":"" })

    else:
        return render(request, "index.pyhtml", {"welcome_string":"Bonjour", })




def ViewAll(request):

    return  
