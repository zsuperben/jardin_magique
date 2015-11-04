import MySQLdb
import MySQLdb.cursors
import getopt
import sys
import socket
import re
import datetime
import ConfigParser
import os
import netaddr

def load_config(file='logger.conf'):
    if not os.path.isfile(file):
        raise ValueError("Config file not found ")
    config = ConfigParser.ConfigParser()
    config.read(file)
    d = {}
    for section in config.sections():
        d[section] = {}
        for i in config.items(section):
            d[section][i[0]] = i[1]

    try:
        if d['sensors']['host_list'][0] is '[':
            d['sensors']['host_list'] = eval(d['sensors']['host_list'])
        else:
            d['sensors']['host_list'] = [ d['sensors']['host_list'] ]

        d['logger']['port'] = int(d['logger']['port'])
    except KeyError:
        return None

    #building a list of valid ips
    temp_list = []
    for host in d['sensors']['host_list']:

        try:
            host = netaddr.IPNetwork(host)
            temp_list.append(host)
        except:
            print("not a valid ip!")

    d['sensors']['host_list'] = temp_list

    print(d)
    return d

def parse_request(request):
    ret_dict = {}
    print(request)
    request = str(request)
    def set_plant(request):
        pm = re.match(r'.*plant=(\d*).*', request)
        if pm:
            ret_dict['plant'] = int(pm.groups()[0])
            print "Got match pm"
            print ret_dict

    def set_soil(request):
        sm = re.match(r'.*soil=(\d*).*', request)
        if sm:
            print "Got match sm"
            ret_dict['soil'] = int(sm.groups()[0])
            print(ret_dict)
    def set_zone(request):
        zm = re.match(r'.*zone=(\d*).*', request)
        if zm:
            ret_dict['zone'] = int(zm.groups()[0])
            print(ret_dict)

    set_plant(request)
    set_soil(request)
    set_zone(request)


    if 'plant' and 'soil' and 'zone' in ret_dict.keys():
        #Adds timestamp
        ret_dict['time'] = "'" + datetime.datetime.now().isoformat(sep=' ') +"'"
        return ret_dict
    else:
        return None

def get_table_for_zone(con, zone):
    if type(con) is not MySQLdb.connections.Connection or type(zone) is not str:
        raise ValueError('Non biloute')

    mycur =con.cursor(MySQLdb.cursors.DictCursor)
    try:
        if mycur.execute("DESCRIBE %s" %  zone) > 0:
            print(mycur.fetchall())
            return True
        else:
            print('False !!! ')
            return False
    except MySQLdb.ProgrammingError:
        return False

def set_table_for_zone(con, zone):
    if type(con) is not MySQLdb.connections.Connection or type(zone) is not str:
        raise ValueError('Non biloute')
    mycur =con.cursor(MySQLdb.cursors.DictCursor)


    req = "CREATE TABLE " + zone + " ( `time` datetime(6) NOT NULL, `plant` smallint(5) NOT NULL, `soil` int(16) NOT NULL, PRIMARY KEY (`time`)  )"
    print(req)
    num = mycur.execute(req)
    print num

    con.commit()


def insert_dict_into_db(connection, table, data):
    if type(connection) is not MySQLdb.connections.Connection:
        raise ValueError("First argument has to be a valid mysql connection object")
    if type(data) is not dict:
        raise ValueError("data has to be of type dict")
    if type(table) is not str:
        raise ValueError("table has to be a string")
    mycur = connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        ret = mycur.execute("DESCRIBE %s ;" % table)
        if ret > 0:
            table_schema = mycur.fetchall()
            list_db =[]
            my_values = '('
            for item in table_schema:
                list_db.append(item['Field'])
            for column in  list_db:
                if column not in data.keys():
                    raise ValueError("dict <=> table mismatch")
                else:
                    my_values = my_values + str(data[column] )+',\n'
            my_values = my_values[:-2] + ')'
    except MySQLdb.MySQLError:
        raise ValueError("Table must be a valid table.")

    # If all of the above checks are passed then we can pretty much dump the thing on the db
    gogetit = "INSERT INTO "+ table +' VALUES '+ my_values +';'
    print(gogetit)
    r = mycur.execute(gogetit)
    connection.commit()

def is_allowed(client, conf):
    allowed = False
    for host in conf['sensors']['host_list']:
        if type(host) is netaddr.ip.IPNetwork:
            if host.__contains__(client):
                allowed = True

        else:
            if host == 'localhost' and client == 'localhost':
                allowed = True

    return allowed

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
