__author__ = 'zsb'
import sys

from tornado_json.requesthandlers import APIError, APIHandler
from tornado_json import schema
import json
import datetime
from  netaddr import IPNetwork
from db import insert_dict_into_db, get_table_for_zone, set_table_for_zone
from config import is_allowed
import logging

class MeasureHandler(APIHandler):
    measure_schema = { "type":"object",
                   "properties":
                        { "zone": {"type":"number"},
                          "soil": {"type":"number"},
                          "temp": {"type":"number"},
                          "plant": {"type":"number"}
                          }}

    def initialize(self, connection=None, Conf=None):
        self.dbc = connection
        myconf =  Conf
        x_real_ip = self.request.headers.get("X-Real-IP")
        self.remote_ip = x_real_ip or self.request.remote_ip
        if not is_allowed(self.remote_ip, myconf):
            raise APIError(401)


    @schema.validate(input_schema=measure_schema)
    def post(self):
        data = {}
        logging.info("New meqsure from %s" % self.remote_ip)
        try:
            #load JSON body
            data = json.loads(self.request.body.decode("utf-8"))
            
            # add some sanity check some day
            data["time"] = "'" + datetime.datetime.now().isoformat() + "'"
            table = "mesure_tbl_" + str(data['zone'])
            if not get_table_for_zone(self.dbc, table):
                set_table_for_zone(self.dbc, table)
            insert_dict_into_db(self.dbc, table, data)




        except Exception as e:
            print("An exception has occured of type : %s, \nIt says : \n%s" % (type(e),e))
            raise APIError(400)

