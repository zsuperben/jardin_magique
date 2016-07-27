from django.views.generic.base import TemplateView
from django.shortcuts import render
from MySQLdb.cursors import DictCursor
import MySQLdb as mdb
from gui_jardin.settings import DATABASES 
class IndexView(TemplateView):
    def get_events(self):
        con = mdb.connect(DATABASES['default']['HOST'],DATABASES['default']['USER'],DATABASES['default']['PASSWORD'],DATABASES['default']['NAME'])
        cur = con.cursor(DictCursor)
        r = cur.execute("SELECT * FROM events ORDER BY time DESC LIMIT 10")
        if r > 0:
            return cur.fetchall()
        else:
            return None

    def get(self, request, *args, **kwargs):
        print("Got there so far")
        a = render(request, "index.html", dictionary={"title": "Welcome to the Djangle !", "events": self.get_events()} )
        print("A little bit further")
        return a

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass
