__author__ = 'zsb'
import re
import datetime


def get_plant(request):
    pm = re.match(r'.*plant=(\d*).*', request)
    if pm:
        return int(pm.groups()[0])


def get_soil(request):
    sm = re.match(r'.*soil=(\d*).*', request)
    if sm:
        return int(sm.groups()[0])

def get_zone(request):
    zm = re.match(r'.*zone=(\d*).*', request)
    if zm:
        return int(zm.groups()[0])

def get_temperature(request):
    tm = re.match(r'.*temp=(-{0,1}\d*\.\d*)', request)
    if tm:
        return float(tm.groups()[0])



def parse_request(request):

    print(request)
    request = str(request)
    lines = request.split('\n')


    retlist = []
    for line in lines:
        # Real parsing happens here.
        d = {}
        #This ugly line is too long and too obscure to read
        d['zone'] = get_zone(request)
        d['plant'] = get_plant(request)
        d['soil'] = get_soil(request)
        d['time'] = "'" + datetime.datetime.now().isoformat(sep=' ') + "'"
        d['temp'] = get_temperature(request)
        if d['zone'] and d['plant'] and d['soil'] and d['time'] and d['temp']:
            retlist.append(d)

    if len(retlist) > 0:
        return retlist
    else:
        return None
