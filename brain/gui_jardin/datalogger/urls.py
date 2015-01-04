from django.conf.urls import url 
from datalogger import views
from datalogger.views import SoilMoistMesure, TempForm, PlantForm, 
urlpattern = [
url(r'^temp/$', views.TempHum.as_view(TempForm),),
]
