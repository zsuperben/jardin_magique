__author__ = 'zsb'
import re
import datetime

def parse_request(request):
    ret_dict = {}
    print(request)
    request = str(request)
    def set_plant(request):
        pm = re.match(r'.*plant=(\d*).*', request)
        if pm:
            ret_dict['plant'] = int(pm.groups()[0])
            print "Got match pm"
            print ret_dict

    def set_soil(request):
        sm = re.match(r'.*soil=(\d*).*', request)
        if sm:
            print "Got match sm"
            ret_dict['soil'] = int(sm.groups()[0])
            print(ret_dict)
    def set_zone(request):
        zm = re.match(r'.*zone=(\d*).*', request)
        if zm:
            ret_dict['zone'] = int(zm.groups()[0])
            print(ret_dict)

    set_plant(request)
    set_soil(request)
    set_zone(request)


    if 'plant' and 'soil' and 'zone' in ret_dict.keys():
        #Adds timestamp
        ret_dict['time'] = "'" + datetime.datetime.now().isoformat(sep=' ') +"'"
        return ret_dict
    else:
        return None
