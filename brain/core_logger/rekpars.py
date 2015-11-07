__author__ = 'zsb'
import re
import datetime

def parse_request(request):

    print(request)
    request = str(request)
    lines = request.split('\n')

    def get_plant(request):
        pm = re.match(r'.*plant=(\d*).*', request)
        if pm:
            return int(pm.groups()[0])
            print "Got match pm"
            print ret_dict

    def get_soil(request):
        sm = re.match(r'.*soil=(\d*).*', request)
        if sm:
            print "Got match sm"
            return int(sm.groups()[0])
            print(ret_dict)
    def get_zone(request):
        zm = re.match(r'.*zone=(\d*).*', request)
        if zm:
            return int(zm.groups()[0])
            print(ret_dict)
    retlist = []
    for line in lines:
        d = {}
        d['zone'], d['plant'], d['soil'], d['time'] = get_zone(request), get_plant(request), get_soil(request), "'" + datetime.datetime.now().isoformat(sep=' ') +"'"
        if d['zone'] and d['plant'] and d['soil'] and d['time']:
            retlist.append(d)

    if len(retlist) > 0:
        return retlist
    else:
        return None
