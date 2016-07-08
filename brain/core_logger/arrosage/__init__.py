from tornado_json.requesthandlers import APIHandler, APIError
from tasks import arrosage, tomates 
from watering import switches, turnOn, turnOff
from db import get_last, get_connection
import MySQLdb

#con = MySQLdb.connect("localhost", "celery", "ffsomg2016",
#                             "jardin")


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
        data['code'] = 200
        data['status'] ="OK"
        data["duration"] = 120
        self.write(data)
