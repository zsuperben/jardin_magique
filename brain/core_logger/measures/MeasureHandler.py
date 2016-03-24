__author__ = 'zsb'
import sys

from tornado_json.requesthandlers import APIError, APIHandler
from tornado_json import schema
import json
import datetime
from  netaddr import IPNetwork
from db import insert_dict_into_db, get_table_for_zone
from config import is_allowed


class MeasureHandler(APIHandler):
    measure_schema = { "type":"object",
                   "properties":
                        { "zone": {"type":"number"},
                          "soil": {"type":"number"},
                          "temp": {"type":"number"},
                          "plant": {"type":"number"}
                          }}

    def initialize(self, environment):
        self.dbc = environment['connection']
        myconf = environment['Conf']
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = x_real_ip or self.request.remote_ip
        if not is_allowed(remote_ip, myconf):
            raise APIError(401)


    @schema.validate(input_schema=measure_schema)
    def post(self):
        data = {}
        try:
            #load JSON body
            data = json.loads(self.request.body.decode("utf-8"))
            # add some sanity check some day
            data["time"] = datetime.datetime.now()
            insert_dict_into_db(self.dbc, get_table_for_zone(self.dbc, data['zone']), data)




        except Exception as e:
            print(e)
            raise APIError(400)

