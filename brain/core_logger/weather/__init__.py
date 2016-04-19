import datetime
import json 
import os
import requests
import logging

url = 'http://api.openweathermap.org/data/2.5/forecast/daily?lat=48.877338&lon=-0.483815&cnt=3&appid=d70b47c0b3a4d2bc343df3973dee2ed0&units=metric'

logger = logging.getLogger('api')

def getWeatherForecast():
    try:
        res = requests.get(url)
        if res.ok:
            obj = json.loads(str(res.text))
            for x in obj['list']:
                x['dt'] = datetime.datetime.utcfromtimestamp(x['dt'])
            return obj
        else:
            logger.error("Invalid HTTP response code : %d" % res.status_code)
            return None
    except KeyError as p:
        logger.error("Invalid JSON returned by Openweathermap : %s " % p)
        logger.debug(res.content)
    except Exception as e:
        logger.error(e)
        return None


def formatted(forecast):

    ret = "Tomorrow %s, the weather will be %s, average temperature should be around : %s degrees celcius." % (forecast['list'][1]['dt'], forecast['list'][1]['weather'][0]['main'], forecast['list'][1]['temp']['day'])
    logger.warning(ret)
    print(ret)
    return ret


