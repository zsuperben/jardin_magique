__author__ = 'zsb'
from tornado_json.requesthandlers import APIError, APIHandler
from ..watering import gpio, switches, turnOn, turnOff
from ..tasks import lightOut


class SwitchHandler(APIHandler):
    def initialize(self):
        pass

    def get(self, *args, **kwargs):
        data = {}

        try:
            if swurl in ("SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7", "SW8"):
                data['switch'] = swurl

        except NameError:
            data['switch'] = json.loads(self.request.body.decode("utf-8"))["switch"]


        self.write('{"code": 200, "status": "OK", "switch": "%s", "state": "%s" }' %(data['switch'], gpio.INPUT(switches[data['switch']])))

    def post(self, *args, **kwargs):
        if self.request.body:
            try:
                print(self.request.body)
                data = json.loads(self.request.body.decode('utf-8'))
            except ValueError:
                print("Error parsing JSON")
                raise APIError(400)
        if data["switch"] not in ("SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7", "SW8"):
            raise APIError(status_code=404,log_message="Wrong switch argument..." )
        if not data["duration"]:
            data["duration"] = 2*60 # 5 minutes
        elif type(data["duration"]) is not int:
            data["duration"] = 2*60 # 5 minutes
        elif data["duration"] > 600:
            data["duration"] = 600

        turnOn(data["switch"])
        lightOut.apply_async(args=[data['switch']], countdown=data['duration'])
        self.write('{"code": 200, "status": "OK", "switch": %s, "duration": %d}' % (data['switch'], data['duration']) )


    def delete(self, *args, **kwargs):
        data = {}
        try:
            if swurl in ("SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7", "SW8"):
                data['switch'] = swurl
        except NameError:
            data['switch'] = json.loads(self.request.body.decode("utf-8"))["switch"]
            print("I get sw = %s" % data['switch'])
        except Exception as e:
            print(e)
            raise APIError(400)

        watering.turnOff(data['switch'])
        self.write('{"status":"OK", "code": 200, "switch": %s}' % data['switch'])

