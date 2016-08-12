import sys
import getopt
from tornado import ioloop
from tornado_json import  application

from db import *

import MySQLdb

from config import load_config,is_allowed

from measures.MeasureHandler import MeasureHandler, wateralert
from switchesManagement import SwitchHandler
from videohandler import VideoHandler
from arrosage import ArrosageHandler, TomatesHandler, CarrottesHandler
from fillup import RemplissageHandler
from sys import path
from os.path import realpath, dirname
from dochandler import DocHandler
path.append(realpath(dirname(__file__)))
import alerter
#TODO add logging configuration to config module
#TODO make server config out of config object 





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
        Conf = load_config("./logger.conf")

    if not Conf:
        sys.stderr.write("Invalid config file.")
        sys.exit(5)

    #Overrides config file value if command line option is passed.
    if dbpassword is not '':
        Conf['db']['password'] = dbpassword

    logger = logging.getLogger('api')
    logger.info("Loading routes")
    toto = application.Application(
        [
            #Backend arduino interface
            (r'/measure/', MeasureHandler, dict(Conf=Conf)),
            (r'/wateralert/', wateralert),
            #Action control
            (r'/switch/(?P<swurl>SW\d)/', SwitchHandler),
            (r'/switch/', SwitchHandler),
            (r'/arrosage/', ArrosageHandler),
            (r'/tomates/', TomatesHandler),
            (r'/remplir/', RemplissageHandler),
            (r'/carrottes/', CarrottesHandler),
            #Frontend reports
            (r'/doc/', DocHandler),
            (r'/video/', VideoHandler),
        ],
        {}
    )
    toto.listen(8888)
    logger.info("Server Starting...")
    ioloop.IOLoop.instance().start()

