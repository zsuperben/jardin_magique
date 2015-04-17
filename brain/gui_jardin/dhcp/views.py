# Create your views here.
from django.template import Template, Context
from django.views.generic import CreateView
from django.shortcuts import render_to_response
from dhcp import models
"""
"""


class CreateConfigView(CreateView):
    """ 
    This class is designed to regroup views around the action of creating a new configuration for the DHCP

    Example de contexte pour remplir le fichier de configuration du DHCP

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

ice comment
    """
   
    def get(self, request, active="y",*args, **kwargs):
        # Do stuff to generate empty view of the forms
        if active is not ("n" or "no"):
            try: 
                rc = models.Config.objects.all()
            style="all"
        else:
            
            try:
                rc = models.Config.Objects.get(active=True)
            style="active"
            
        except AttributeError, DatabaseError as e:
                print("The get request on the DB seems to fail with a non-eexisting field somewhere : %s" % e )
                render_to_response(ERROR_TEMPLATE, {"str":"The get request on the DB seems to fail with a non-eexisting field somewhere : %s" % e, "err":e })        
                return 255
        
        if style is "active":
            render_to_response(CONFIG_TEMPLATE, {"style":"active","config":**rc})
        elif style is "all":
            render_to_response(CONFIG_TEMPLATE, {"style":"all", "config" : *rc })

        
        return 1  # END of GET  function 



    def post(self, request, *args, **kwargs):
        # Do stuff to validate form data.
        return 1 
    def form_valid(self, form, *arg, **kwargs):
        # Do stuff to save object 
        return 1
