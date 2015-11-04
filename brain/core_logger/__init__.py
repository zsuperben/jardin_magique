import MySQLdb
import MySQLdb.cursors
import getopt
import sys
import socket

from db import get_table_for_zone, set_table_for_zone, insert_dict_into_db
from config import load_config,is_allowed
from rekpars import parse_request






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

    try:
        Conf = load_config(configfile)
    except NameError:
        Conf = load_config()

    if not Conf:
        sys.stderr.write("Invalid config file.")
        sys.exit(5)

    try:
        if not 'db' or not 'logger' or not 'sensors' in Conf.keys():
            raise Exception("Config file is incomplete or corrupted")


        c= MySQLdb.connect(Conf['db']['host'],
                           Conf['db']['user'],
                           Conf['db']['password'],
                           Conf['db']['db'])

        cur = c.cursor()
        s = socket.socket()
        s.bind((Conf['logger']['address'], Conf['logger']['port']))
        s.listen(10)


        #Building host list from what is in the config file


    except AttributeError as e:
        sys.stderr.write("Incomplete Configuration file ! %s" % str(e))
        raise e


    while True:
            client, address = s.accept()
            my_request = client.recv(8192)
            client.close()
            host, port = address
            print("Got : " + my_request)

            if is_allowed(host, Conf):
                print("OK parsing request")
                tutu = parse_request(my_request)
            else:
                print("Not in host list")
            try:
                print("tries to insert : %s" % tutu)
                if tutu:
                    if tutu['zone']:
                        zone = 'mesure_tbl_' + str(tutu.pop('zone'))
                        print('popped zone')
                    else:
                        print("NULL REQUEST : NO ZONE !")
                        continue
                    if get_table_for_zone(c, zone):
                        print('here')
                        insert_dict_into_db(c, zone, tutu)
                    else:
                        print('else')
                        set_table_for_zone(c, zone)
                        insert_dict_into_db(c, zone, tutu)
                else:
                    print("NULL REQUEST!")
            except NameError:
                print("No data!")
