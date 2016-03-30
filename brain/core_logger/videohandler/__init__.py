from tornado.web import RequestHandler, HTTPError
import datetime 
import cv2
import os

cam = cv2.VideoCapture(0)

class VideoHandler(RequestHandler):
    
    def initialize(self):
        ret, self.tmp = cam.read()
        if ret:
            self.fname = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M.png")
            cv2.imwrite(self.fname, self.tmp)
        else:
            raise HTTPError(500)


    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "image/png")
        with open(self.fname, 'rb') as f:
            [ self.write(f.read(1)) for x in range(os.path.getsize(self.fname)) ]

