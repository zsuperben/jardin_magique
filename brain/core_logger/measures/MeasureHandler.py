__author__ = 'zsb'
import sys
import alerter
from tornado_json.requesthandlers import APIError, APIHandler
from tornado_json import schema
import json
import datetime
from  netaddr import IPNetwork
from db import insert_dict_into_db, get_table_for_zone, set_table_for_zone, get_connection

from config import is_allowed
import logging

logger = logging.getLogger('api')

class MeasureHandler(APIHandler):
    measure_schema = { "type":"object",
                   "properties":
                        { "zone": {"type":"number"},
                          "soil": {"type":"number"},
                          "temp": {"type":"number"},
                          "plant": {"type":"number"}
                          }}

    def initialize(self, Conf=None):
        self.dbc = get_connection()
        myconf =  Conf
        x_real_ip = self.request.headers.get("X-Real-IP")
        self.remote_ip = x_real_ip or self.request.remote_ip
        if not is_allowed(self.remote_ip, myconf):
            raise APIError(401)

    @schema.validate(input_schema=measure_schema)
    def post(self):
        data = {}
        logger.info("New measure from %s" % self.remote_ip)
        try:
            #load JSON body
            data = json.loads(self.request.body.decode("utf-8"))
            
            # add some sanity check some day
            data["time"] =  datetime.datetime.now().isoformat()
            table = "mesure_tbl_" + str(data['zone'])
            if not get_table_for_zone(self.dbc, table):
                set_table_for_zone(self.dbc, table)
            insert_dict_into_db(self.dbc, table, data)


        except Exception as e:
            logger.error("An exception has occured of type : %s, \nIt says : \n%s" % (type(e),e))
            raise APIError(500)

    def on_finish(self):
        self.dbc.close()


lastmail = datetime.datetime.now() - datetime.timedelta(days=1)
etat = 'Unknown'
class wateralert(APIHandler):
    def get(self):
        self.write({'lastmail': lastmail,'etat': etat })

    def post(self):
        # todo lire JSON
        global lastmail, etat
        oldstate = etat

        try:
            data = json.loads(self.request.body.decode("utf-8"))
            logger.warning(self.request.body.decode("utf-8"))
            etat = data['etat']
        
            if etat != oldstate or datetime.datetime.now() - lastmail > datetime.timedelta(days=1):
                s = "l'eau est %s" % "pleine" if etat else "pas pleine" 
                alerter.alert(s)
                logger.error("mail envoye : %s" % s )
                lastmail = datetime.datetime.now()
            else:
                logger.warning("l'eau est %s" % "pleine" if etat else "pas pleine")
        except Exception as e:
            logger.error("Shit happens : %s" % e)
            raise APIError(500)

