from tornado_json import APIHandler, APIError
from db import *
from videohandler import get_latest_pic


class ReportHandler(APIHandler):
    def get(self, *args, **kwargs):
        bob = {}
        bob['measures'] = get_measures()
        bob['events'] = get_last(get_connection(), thing=None, limit=20)
        bob['img'] = get_latest_pic()
        self.write()
