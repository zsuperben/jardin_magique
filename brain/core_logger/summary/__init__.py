from tornado_json import APIHandler, APIError
import MySQLdb as mdb
from MySQLdb.cursors import DictCursor
from db import executeSQL
import logging

mylog = logging.getLogger("api")

class SummaryHandler(APIHandler):
    def initialize(self, con):
        self.con = con
        self.cur = con.cursor(class=DictCursor)
        self.set_header("Content-Type", "application/json")

    def get(self, *args, **kwargs):
        r = executeSQL(self.cur, "SELECT * FROM mesure_tbl_1 ORDER BY time DESC LIMIT 1")
        d = None
        if r > 0:
            d = self.cur.fetchall()

        try:
            fh = open('/var/run/jardin/waterlvl', 'r')
            for line in fh:
                pass
            d['last_filled'] = line 
            fh.close()
        except IOError:
            d['last_filled'] = 'unknown'
        try: 
            fh = open('/var/run/jardin/arrosage', 'r')
            for line in fh:
                pass
            d['last_watered'] = line 
            fh.close()
        except IOError:
            d['last_watered'] = "unknown"
        mylog.debug(str(d))
 
        self.write(d)
