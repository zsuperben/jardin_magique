__author__ = 'zsb'
from configparser import ConfigParser
import os
import netaddr
import logging

logger = logging.getLogger('api')

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
        d[logging]
        #TODO actually load config from file.
    except KeyError:
        #No specific logging config was given: setting up default values:
        fh = logging.FileHandler('/var/log/jardin/api.log')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        logger.addHandler(fh)
        logger.addHandler(ch)



    try:
        if d['sensors']['host_list']:
            logger.info(d['sensors']['host_list'].split(' '))
            d['sensors']['host_list'] = d['sensors']['host_list'].split(' ')
        else:
            raise KeyError("Incomplete config file !")

        d['logger']['port'] = int(d['logger']['port'])

        fh = open(d['logger']['logfile'], 'a')
        fh.close()

    except ( KeyError, IOError ) as e:
        logger.error(str(e))
        return None

    #building a list of valid ips
    temp_list = []
    for host in d['sensors']['host_list']:

        try:
            host = netaddr.IPNetwork(host)
            temp_list.append(host)
        except:
            logger.error("not a valid ip! %s" % host)

    d['sensors']['host_list'] = temp_list

    try:
        d['alerts']['mail']

        # Ensure d[alerts][to] is a list
        d['alerts']['to'] = d['alerts']['to'].split(' ')
    except KeyError as e:
        logger.error('invalid alerts section in configuration: %s' % e)
        return None
    
    logger.debug(str(d))
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
    logger.info("Client is %s   and  hostlist is %s, Client is allowed : %s" %
          ( client, conf['sensors']['host_list'], allowed )
          )
    return allowed
