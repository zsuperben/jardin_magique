__author__ = "zsb"

from tornado_json.requesthandlers import APIError, APIHandler
from tornado import schema
import json
import datetime
from db import insert_dict_into_db, get_connection
import requests

APPID = "d70b47c0b3a4d2bc343df3973dee2ed0"

def meteoHandler(APIHandler):
    def get(self):
        try:
            pluie = 0 
            m = requests.get("http://api.openweathermap.org/forecast?q=cahan,fr&appid=%s&units=metric&lang=fr" % APPID )
            if m.response_code == 200:
                d = json.loads(m.content.decode())
                for prev in d['list']:
                    if 'rain' in prev.keys():
                        pluie = pluie + prev['rain']['3h']

            self.write({"pluie": pluie})
        except:
            raise APIError(500)
