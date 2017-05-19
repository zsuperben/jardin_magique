__author__ = "zsb"

from tornado_json.requesthandlers import APIError, APIHandler
import json
import datetime
from db import insert_dict_into_db, get_connection
import requests
import logging

logger = logging.getLogger('api')

APPID = "d70b47c0b3a4d2bc343df3973dee2ed0"

class meteoHandler(APIHandler):
    def get(self):
        try:
            pluie = 0 
            m = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=cahan,fr&appid=d70b47c0b3a4d2bc343df3973dee2ed0&units=metric&lang=fr")
            if m.status_code == 200:
                d = json.loads(m.content.decode())
                for prev in d['list']:
                    print(prev, '\n')
                    if 'rain' in prev.keys():
                        if '3h' in prev['rain'].keys():
                            pluie = pluie + prev['rain']['3h']
            else:
                print("Got some issues getting the thing : status %d" % m.status_code)
            self.write({"pluie": pluie})
        except Exception as e:
            logger.error(e)
            raise APIError(500)
