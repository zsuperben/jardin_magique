from tornado.web import RequestHandler, HTTPError
import datetime 
import cv2
import os
import logging 
import base64

logger = logging.getLogger('api')
logger.error('Starting up video camera...')

cam = cv2.VideoCapture(0)
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

def get_latest_pic(b64=True):
    '''
    Takes no argument and return a base64 encoded png image. Should always be the latest picture. 
    '''
    path = get_path()
    try:
        lst = os.listdir(path).sort()
    except FileNotFoundError:
        return None
    if b64:
        try:
            fh = open(lst[-1], 'r')
        except:
            logger.error("Could not read picture from disk")
            return None
        return base64.b64encode(fh.read())
    else:
        return lst[-1]


def get_path():
#    global Conf
#    print(Conf)
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    try:
        picdir = Conf['pictures']['picdir']
    except (Exception, KeyError):
        picdir = "/opt/disk/jardin"
    return os.path.join(picdir, today_str)


def take_picture():
    try:
        ret, tmp = cam.read()
        fname = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M.png")
        folder = get_path()
        if not os.path.isdir(folder):
            os.mkdir(folder)
        full_name = os.path.join(folder, fname)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        cv2.imwrite(full_name, tmp)
        return full_name
    except IOError as e:
        logger.error("Could not write picture to disk : %s" % e)
        return None


class VideoHandler(RequestHandler):
    
    def initialize(self):
        self.fname = take_picture()
        if not self.fname:
            raise APIError(500)

    def get(self, *args, **kwargs):
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = x_real_ip or self.request.remote_ip

        self.set_header("Content-Type", "image/png")
        logger.error("Taking a picture and sending it to %s" % remote_ip)
        with open(self.fname, 'rb') as f:
            [self.write(f.read(1)) for x in range(os.path.getsize(self.fname))]
