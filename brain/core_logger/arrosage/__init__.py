from tornado_json.requesthandlers import APIHandler, APIError
from tasks import arrosage, tomates 
from watering import switches, turnOn, turnOff
from db import get_last, get_connection
import MySQLdb

#con = MySQLdb.connect("localhost", "celery", "ffsomg2016",
#                             "jardin")
import logging 
mylogger = logging.getLogger('api')

class ArrosageHandler(APIHandler):
    def get(self):
        data = {}
        self.set_header("Content-Type", "application/json")
        data['code'] = 200
        data['status'] = 'OK'
        con = get_connection()
        data['last'] = get_last(con, "seeds") # todo get last time from DB
        con.close()
        self.write(data)


    def put(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        data = {}
        data['code'] = 200
        data['status'] = 'OK'
        data['duration'] = 120
        arrosage.apply_async([], countdowon=1)
        self.write(data)


class TomatesHandler(APIHandler):
    def get(self):
        data = {}
        self.set_header("Content-Type", "application/json")
        data['code'] = 200
        data['status'] = 'OK'
        con = get_connection()
        data['last'] = get_last(con, "tomates") # todo get last time from DB
        con.close()
        self.write(data)


    def put(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        data = {}
        data['code'] = 200
        data['status'] = 'OK'
        data['duration'] = 120
        tomates.apply_async([], countdowon=1)
        self.write(data)


class CarrottesHandler(APIHandler):
    def get(self):
        data = {}
        self.set_header("Content-Type","application/json")
        data['code'] = 200
        data['status'] = "ok"
        con = get_connection()
        data['last'] = get_last(con, "exterior")
        con.close()
        self.write(data)

    def put(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        data = {}
        try:
            data['code'] = 200
            data['status'] ="OK"
            data["duration"] = 120
            r = ext_arrosage.apply_async([], countdown=1 )
        except err:
            data['code'] = 500
            data['status'] = "Failure"
            data['duration'] = 0
            mylogger.error("Failed to send task with error : %s" % err)            
        self.write(data)
