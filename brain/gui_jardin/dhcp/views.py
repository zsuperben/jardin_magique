# Create your views here.
from django.template import Template, Context
from django.views.generic import CreateView

"""
Example de contexte pour remplir le fichier de configuration du daemon dhcp 

c = [
    {'networks_list': 
        [
            {
                'startip': '10.69.0.55', 
                'netmask': '255.255.0.0', 
                'endip': '10.69.0.155', 
                'netboot': {
                    'filename': 'pxelinux.0', 
                    'server': '10.69.0.1'
                    }, 
                'netaddr': '10.69.0.0', 
                'gateway': '10.69.0.1', 
            }, 
            {
                'netmask': '255.255.255.224', 
                'netaddr': '10.123.224.0'
            }
         ], 
     'dns': 'jardin-magique.org', 
     'rpi': {
            'ip': '10.69.0.1', 
            'name': 'bob'
            }, 
     'default_lease_time': 6000, 
     'sensors_list': [
        {
            'ip': '10.17.0.252', 
            'nom': 'toto', 
            'ethernet': 'F4:55:65:33:4B:FF'
        },{
            'ip': '10.17.0.253', 
            'nom': 'titi', 
            'ethernet': 'F4:55:65:33:4C:FF'
        }], 
     'logfacility': 'local7', 
     'max_lease_time': 72000
     
     }]

"""
class CreateConfigView(CreateView):

    def get(self, request, *args, **kwargs):
        # Do stuff to generate empty view of the forms


    def post(self, request, *args, **kwargs):
        # Do stuff to validate form data.

    def form_valid(self, form, *arg, **kwargs):
        # Do stuff to save object 
