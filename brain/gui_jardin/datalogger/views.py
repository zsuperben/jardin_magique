from django.shortcuts import render
from djanggo.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django import forms


# Create your views here.
def record_mesure(request):
    if request.method == 'POST' && "plant", "time", "value", "sec" in request.POST:
        if request.POST
        
