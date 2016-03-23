from celery import Celery, Task
import watering



app = Celery()

class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@app.task(base=CallbackTask)
def lightOut(sw):    
    return watering.turnOff(sw)


