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

logging.basicConfig(filename="/var/log/jardin/")

app = Celery()
app.conf.CELERY_TIMEZONE = 'Europe/Paris'
app.conf.CELERYBEAT_SCHEDULE = {
    'TurnOnTheLight': {
        'task': 'tasks.lightOut',
        'schedule': crontab(hour=6),
        'args': "SW7"
    },
    "Switchitoff": {
        'task': 'tasks.lightUp',
        'scheadule': crontab(hour=0),
        'args': "SW7"
        
        }
}

MIN_SOIL = 80


class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@app.task(base=CallbackTask)
def lightOut(sw):    
    return watering.turnOff(sw)
@app.task(base=CallbackTask)
def lightUp(sw):
    return watering.turnOn(sw)
#
#
#@app.task(base=CallbackTask)
#def CheckForAction():
#    # first get all the measur tables.
#    yesterday = datetime.datetime.now() - timedelta(days=1)
#    mycur = connection.cursor()
#    ntbl= mycur.execute("SHOW TABLES LIKE 'mesure_tbl_%'")
#    if ntbl >0:
#        tables = mycur.fetchall()
#        for table in tables:
#            req = "SELECT soil FROM " + table[0] + " WHERE  `time` >= '%s' " % yesterday.isoformat()
#            l = mycur.execute(req)
#            measures = mycur.fetchall()
#            avg = 0
#            for m in measures:
#                avg += m[0]
#            avg =  avg / l
#            if avg <= MIN_SOIL:
#                waterIsNeeded = True
#                logging.warning("Water is needed, average is %d" % avg)
#
#    else:
#        logging.warning("No measures detected !")
#
#
#
#def CalculAvg():
#    pass
#
#
#
    
