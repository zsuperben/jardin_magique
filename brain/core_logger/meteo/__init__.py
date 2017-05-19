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
            m = requests.get("http://api.openweathermap.org/forecast?q=cahan,fr&appid=%s&units=metric&lang=fr" % APPID )
            if m.status_code == 200:
                print(m.content.decode())
                d = json.loads(m.content.decode())
                logger.notice(d)
                for prev in d['list']:
                    if 'rain' in prev.keys():
                        pluie = pluie + prev['rain']['3h']
            else:
                print("Got some issues getting the thing : status %d" % m.status_code)
            self.write({"pluie": pluie})
        except Exception as e:
            logger.error(e)
            raise APIError(500)
