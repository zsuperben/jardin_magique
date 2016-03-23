import  json
from tornado_json.requesthandlers import APIHandler, APIError 
from tornado_json import schema
import logging

import sys
import getopt
from tornado import ioloop
from tornado_json import  application

from db import *

import MySQLdb

from config import load_config,is_allowed

import watering
from celery import signature
import tasks
import datetime


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

        watering.turnOn(data["switch"])
        tasks.lightOut.apply_async(args=[data['switch']], countdown=data['duration'])
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


measure_schema = { "type":"object",
                   "properties":
                        { "zone": {"type":"number"},
                          "soil": {"type":"number"},
                          "temp": {"type":"number"},
                          "plant": {"type":"number"}
                          }}

class MeasureHandler(APIHandler):
    def initialize(self):
        pass    
    
    @schema.validate(input_schema=measure_schema)
    def post(self):
        data = {}
        try:
            #load JSON body
            data = json.loads(self.request.body.decode("utf-8"))
            # add some sanity check some day
            data["time"] = datetime.datetime.now()
            insert_dict_into_db(connection, get_table_for_zone(connection, data['zone']), data)
                

         
         
        except Exception as e:
            print(e)
            raise APIError(400)


if __name__ == "__main__":
    opt, trash = getopt.getopt(args=sys.argv[1:],
                               shortopts="p:c:",
                               longopts=['password', 'config'])
    dbpassword = ''
    configfile = ''
    for o,a in opt:
        if o in ("-p", "--password"):
            dbpassword = a
        elif o in ("-c", "--config"):
            configfile = a
        else:
            print("either no password supplied or wrong options")
            sys.exit(5)

    if configfile is not '':
        Conf = load_config(configfile)
    else:
        Conf = load_config("/etc/jardin/logger.conf")

    if not Conf:
        sys.stderr.write("Invalid config file.")
        sys.exit(5)

    #Overrides config file value if command line option is passed.
    if dbpassword is not '':
        Conf['db']['password'] = dbpassword


    connection = MySQLdb.connect(Conf['db']['host'],
                               Conf['db']['user'],
                               Conf['db']['password'],
                               Conf['db']['db'])



    toto = application.Application(
        [
            (r'/measure/', MeasureHandler),
            (r'/switch/(?P<swurl>\d)/', SwitchHandler),
            (r'/switch/', SwitchHandler),
        ],
        {}
    )
    toto.listen(8888)
    ioloop.IOLoop.instance().start()


