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
light.append("SW7")


app.conf.CELERYBEAT_SCHEDULE = {
    'TurnOffTheLight': {
        'task': 'tasks.lightOut',
        'schedule': crontab(hour=0),
        'args': light
    },
    "Switchiton": {
        'task': 'tasks.lightUp',
        'schedule': crontab(hour=6),
        'args': light
        
        }
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
    return watering.turnOff(sw)


@app.task(base=CallbackTask)
def lightUp(sw, *args, **kwargs):
    return watering.turnOn(sw)


WaterIsNeeded = False

@app.task(base=CallbackTask)
def CheckForAction():
    allAverages  = CalculAvg()
    if not allAverages:
        logging.error("Can't tell if water is needed : no measures ")

   
    for avg in allAverages:
        if allAverages[avg] <= MIN_SOIL:
            waterIsNeeded = True
            logging.warning("Water is needed in zone : '%s' average is %d" % (avg)




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
