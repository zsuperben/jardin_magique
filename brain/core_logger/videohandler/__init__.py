from tornado.web import RequestHandler, HTTPError
import datetime 
import cv2
import os
import logging 

logger = logging.getLogger('api')
logger.error('Starting up video camera...')

cam = cv2.VideoCapture(0)
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )



class VideoHandler(RequestHandler):
    
    def initialize(self):
        ret, self.tmp = cam.read()
        x_real_ip = self.request.headers.get("X-Real-IP")
        self.remote_ip = x_real_ip or self.request.remote_ip

        if ret:
            self.fname = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M.png")
            cv2.imwrite(self.fname, self.tmp)
        else:
            raise HTTPError(500)


    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "image/png")
        logger.error("Taking a picture and sending it to %s" % self.remote_ip)
        with open(self.fname, 'rb') as f:
            [ self.write(f.read(1)) for x in range(os.path.getsize(self.fname)) ]

