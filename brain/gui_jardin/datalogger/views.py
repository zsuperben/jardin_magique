from django.views.generic.base import TemplateView
from django.shortcuts import render
from MySQLdb.cursors import DictCursor
import MySQLdb as mdb
from gui_jardin.settings import DATABASES 
from base64 import b64encode
import datetime

def get_image():
    try: 
        #list current avalaible photos
        fh  = open('/home/pi/jardin_magique/brain/core_logger/2016_07_26_19_02.png', 'r')
        data = fh.read()
    except:
        return None
    return b64encode(data)

def get_failures():
    return [
            {
                "time": datetime.datetime.now(), 
                "name": "FAlche error1", 
                "exception": "Un beau petit text bien mytho"
            }, {
                "time": datetime.datetime.now() -datetime.timedelta(hours=5), 
                "name": "obi",
                "exception": "La meme ma gueule"}]





class IndexView(TemplateView):
    def get_cursor(self):
        con = mdb.connect(DATABASES['default']['HOST'],DATABASES['default']['USER'],DATABASES['default']['PASSWORD'],DATABASES['default']['NAME'])
        cur = con.cursor(DictCursor)
        return cur

    def get_events(self):
        cur = self.get_cursor()
        r = cur.execute("SELECT * FROM events ORDER BY time DESC LIMIT 10")
        if r > 0:
            return cur.fetchall()
        else:
            return None


    def get_measures(self):
        cur = self.get_cursor()
        r = cur.execute("SHOW TABLES LIKE 'mesure_tbl_%'")
        my_values = []
        if r > 0:
            tables = cur.fetchall()
            #print("Tables contains : %s and is type %s" % (tables, type(tables)))
            for t in tables:
                print(t.values())
                r = cur.execute("SELECT * FROM %s ORDER BY TIME DESC LIMIT 10 "%t.values()[0] )
                if r > 0:
                    tmp = cur.fetchall()
                    for v in tmp:
                        my_values.append(v)

        return my_values

    def get(self, request, *args, **kwargs):
        print("Got there so far")
        context = {
            "title": "Welcome to the Djangle !", 
            "events": self.get_events(), 
            "image": get_image(), 
            'tasks': get_failures(),
            "measures": self.get_measures(),
            } 
        a = render(request, "index.html", context=context)
        print("A little bit further")
        return a

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwa11rgs):
        pass
