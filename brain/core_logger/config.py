__author__ = 'zsb'
import ConfigParser
import os
import netaddr

def load_config(file='logger.conf'):
    if not os.path.isfile(file):
        raise Exception("Config file not found ")
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

        fh = open(d['logger']['logfile'], 'a')
        fh.close()

    except KeyError, IOError:
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

    return allowed
