import sys
import getopt
from tornado import ioloop
from tornado_json import  application

from db import *

import MySQLdb

from config import load_config,is_allowed

from measures.MeasureHandler import MeasureHandler
from switchesManagement import SwitchHandler
from videohandler import VideoHandler
from arrosage import ArrosageHandler
from fillup import RemplissageHandler
from sys import path
from os.path import realpath, dirname
path.append(realpath(dirname(__file__)))

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
        Conf = load_config("/etc/jardin/logger.conf")

    if not Conf:
        sys.stderr.write("Invalid config file.")
        sys.exit(5)

    #Overrides config file value if command line option is passed.
    if dbpassword is not '':
        Conf['db']['password'] = dbpassword


    connection= MySQLdb.connect(Conf['db']['host'],
                               Conf['db']['user'],
                               Conf['db']['password'],
                               Conf['db']['db'])



    toto = application.Application(
        [
            (r'/measure/', MeasureHandler, dict(connection=connection, Conf=Conf)),
            (r'/switch/(?P<swurl>SW\d)/', SwitchHandler),
            (r'/switch/', SwitchHandler),
            (r'/video/', VideoHandler),
            (r'/arrosage/', ArrosageHandler),
            (r'/remplir/', RemplissageHandler),
        ],
        {}
    )
    toto.listen(8888)
    ioloop.IOLoop.instance().start()


