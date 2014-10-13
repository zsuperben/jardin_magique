# Create your views here
from django.shortcuts import render
from core.models import Plant
def index(request):
    return render(request, "index.pyhtml", {"welcome_string":"Super string ficelle", "list": Plant.objects.all() })




    
