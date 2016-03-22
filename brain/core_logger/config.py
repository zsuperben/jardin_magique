__author__ = 'zsb'
#import ConfigParser
from configparser import ConfigParser
import os
import netaddr

def load_config(file='logger.conf'):
    if not os.path.isfile(file):
        raise Exception("Config file not found ")
    config = ConfigParser()
    config.read(file)
    d = {}
    for section in config.sections():
        d[section] = {}
        for key, val in config.items(section):
            d[section][key] = val

    try:
        if d['sensors']['host_list']:
            print(d['sensors']['host_list'].split(' '))
            d['sensors']['host_list'] = d['sensors']['host_list'].split(' ')
        else:
            raise KeyError("Incomplete config file !")

        d['logger']['port'] = int(d['logger']['port'])

        fh = open(d['logger']['logfile'], 'a')
        fh.close()

    except ( KeyError, IOError ):
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

def is_allowed(client, conf):
    allowed = False
    for host in conf['sensors']['host_list']:
        if type(host) is netaddr.ip.IPNetwork:
            if host.__contains__(client):
                allowed = True

        else:
            if host == 'localhost' and client == 'localhost':
                allowed = True
    print("Client is %s   and  hostlist is %s" % ( client, conf['sensors']['host_list'] ))
    return allowed
