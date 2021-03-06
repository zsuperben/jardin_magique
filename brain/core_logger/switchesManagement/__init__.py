__author__ = 'zsb'
from tornado_json.requesthandlers import APIError, APIHandler
from watering import gpio, switches, turnOn, turnOff
from tasks import lightOut
import json
import logging

logger = logging.getLogger('api')

class SwitchHandler(APIHandler):
    def initialize(self):
        self.set_header("Content-Type","application/json")        
        pass

    def get(self, *args, **kwargs):
        data = {}
        data["code"] = 200
        data["status"] = "OK"
        
        try:
            if swurl in switches.keys():
                data['switch'] = swurl
            else:
                raise APIError(400)

            data['state'] = gpio.input(swurl)


        except NameError:
            #msg = '{"code":200, "status": "OK", "switch": {'
            data['switch'] = {}
            for key in switches:
                #msg = msg + '"%s" : "%s", ' % (key, gpio.input(switches[key]))
                data['switch'][key] = gpio.input(switches[key])
            #msg = msg + '}}'

        self.write(data)

    def post(self, *args, **kwargs):
        if self.request.body:
            try:
                logger.debug(self.request.body)
                data = json.loads(self.request.body.decode('utf-8'))
            except ValueError:
                logger.error("Error parsing JSON")
                raise APIError(400)
        if data["switch"] not in switches.keys():
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
            if swurl in switches.keys():
                data['switch'] = swurl
        except NameError:
            data['switch'] = json.loads(self.request.body.decode("utf-8"))["switch"]
            logger.debug("I get sw = %s" % data['switch'])
        except Exception as e:
            logger.error(e)
            raise APIError(400)
        logger.warning("Turning off %s" % data['switch'])
        turnOff(data['switch'])
        self.write('{"status":"OK", "code": 200, "switch": %s}' % data['switch'])

