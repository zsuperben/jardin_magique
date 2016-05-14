from tornado_json.requesthandlers import APIHandler, APIError
from tasks import arrosage
from watering import switches, turnOn, turnOff




class ArrosageHandler(APIHandler):
    def get(self):
        data = {}
        self.set_header("Content-Type", "application/json")
        data['code'] = 200
        data['status'] = 'OK'
        data['last'] = 'unknown' # todo get last time from DB
        self.write(data)


    def put(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        data = {}
        data['code'] = 200
        data['status'] = 'OK'
        data['duration'] = 120
        arrosage.apply_async([], countdowon=1)
        self.write(data)


class CarrottesHandler(APIHandler):
    def get(self):
        data = {}
        self.set_header("Content-Type","application/json")
        data['code'] = 200
        data['status'] = "ok"
        data['last'] = 'unknown'
        self.write(data)

    def put(self, *args, **kwargs):
        self.set_header("Content-type", "application/json")
        data = {}
        data['code'] = 200
        data['status'] ="OK"
        data["duration"] = 120
        self.write(data)