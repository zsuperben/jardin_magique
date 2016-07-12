from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from MySQLdb.cursors import DictCursor
import MySQLdb as mdb

class IndexView(TemplateView):
    def get_events(self):
        con = mdb.connect("localhost", "celery", "", "jardin")
        cur = con.cursor(DictCursor)
        r = cur.execute("SELECT * FROM events ORDER BY time DESC LIMIT 10")
        if r > 0:
            return cur.fetchall()
        else:
            return None

    def get(self, request, *args, **kwargs):
        return render_to_response(request, template_name="index.html",{"title": "Welcome to the Djangle !", "events": self.get_events()} )