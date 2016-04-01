from celery import Celery, Task
import watering

from datetime import timedelta
from celery.schedules import crontab
import logging


import MySQLdb


connection = MySQLdb.connect("localhost",
                             "celery",
                             "ffsomg2016",
                             "jardin")

logging.basicConfig(filename="/var/log/jardin/celery")

app = Celery()
app.conf.CELERY_TIMEZONE = 'Europe/Paris'




light =[]
light.append( "SW7")
olight = []
olight.append("SW5")

app.conf.CELERYBEAT_SCHEDULE = {
    'TurnOffTheLight': {
        'task': 'tasks.lightOut',
        'schedule': crontab(hour=0, minute=0),
        'args': light
    },
    "Switchiton": {
        'task': 'tasks.lightUp',
        'schedule': crontab(hour=6, minute=0),
        'args': light
        
        },
    "thatOtherLightOn":{
        'task': 'tasks.lightUp',
        'schedule': crontab(hour=6, minute=5),
        'args': olight,
    },    
    'TurnOffTheoLight': {
        'task': 'tasks.lightOut',
        'schedule': crontab(hour=0, minute=0),
        'args': olight
    },
    'moveAirAround': {
        'task': 'tasks.ventilation',
        'schedule': timedelta(minutes=30),
        'args': (),
    },
    'PutWaterOnSeeds': {
        'task': 'tasks.arrosage',
        'schedule': timedelta(hours=12),
        'args': (),
    },
 
}

MIN_SOIL = 80


class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        logging.info(
            'Successfully ran %s' % str(task_id)
        )

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.error(
            'Failed to run %s' % str(task_id)
        )


@app.task(base=CallbackTask)
def lightOut(sw, *args, **kwargs):    
    if type(sw) is list:
        return [ watering.turnOff(x) for x in sw ]
    else:
        return watering.turnOff(sw)


@app.task(base=CallbackTask)
def lightUp(sw, *args, **kwargs):
    if type(sw) is list:
        return [ watering.turnOn(x) for x in sw ]
    else:
        return watering.turnOn(sw)



@app.task(base=CallbackTask)
def CheckForAction():
    WaterIsNeeded = False
    allAverages  = CalculAvg()
    if not allAverages:
        logging.error("Can't tell if water is needed : no measures ")

   
    for avg in allAverages:
        if allAverages[avg] <= MIN_SOIL:
            waterIsNeeded = True
            logging.warning("Water is needed in zone : '%s' average is %d" % (avg))



def CalculAvg():
    # first get all the measure tables.
    retdic = {}
    yesterday = datetime.datetime.now() - timedelta(days=1)
    mycur = connection.cursor()
    ntbl= mycur.execute("SHOW TABLES LIKE 'mesure_tbl_%'")
    if ntbl >0:
        tables = mycur.fetchall()
        for table in tables:
            req = "SELECT soil FROM `" + table[0] + "` WHERE  `time` >= '%s' " % yesterday.isoformat()
            l = mycur.execute(req)
            if l > 0:
                measures = mycur.fetchall()
            else:
                logging.warning("Can't get measures from yesterday : empty set.")
                continue

            avg = 0
            for m in measures:
                avg += m[0]
            avg =  avg / l
            retdic[table[0]] = avg

    else:
        logging.warning("No measures detected at all.")
        return None
    
    return retdic    


@app.task(base=CallbackTask)
def ventilation():
    logging.info("Ventilation on for 20 seconds")
    watering.turnOff("SW9")
    lightUp.apply_async(["SW9"], countdown=20)


@app.task(base=CallbackTask)
def arrosage():
    logging.warning("Turning on watering for two minutes")
    watering.turnOn("SW6")
    lightOut.apply_async(["SW6"], countdown=20)


@app.task(base=CallbackTask)
def remplissage_cuve():
    logging.warning("Filling up the water tank on 1st floor")
    watering.turnOn("SW4")
    watering.turnOn("SW8")
    lightOut.apply_async( [ ["SW8", "SW4"] ], countdown=10)


