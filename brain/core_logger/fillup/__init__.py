from tornado_json.requesthandlers import APIHandler, APIError
from tasks import remplissage_cuve
from watering import switches, turnOn, turnOff
from os.path import isfile
from db import get_connection, get_last


class RemplissageHandler(APIHandler):
    def initialize(self):
        if not isfile('/var/run/jardin/waterlvl'):
            open('/var/run/jardin/waterlvl', 'w')

    def get(self):
        data = {}
        self.set_header("Content-Type", "application/json")
        data['code'] = 200
        data['status'] = 'OK'
        try:
            f = open('/var/run/jardin/waterlvl')
            for line in f:
                pass
            if line == '':
                line = 'unknown-blanck'
            data['last'] = unicode(line)
        except IOError:
            con = get_connection()
            data['last'] = get_last(con, "remplir")
        self.write(data)


    def put(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        data = {}
        data['code'] = 200
        data['status'] = 'OK'
        data['duration'] = 30
        remplissage_cuve.apply_async([], countdowon=1)
        self.write(data)
