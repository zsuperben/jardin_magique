from tornado.web import RequestHandler
import cv2


class VideoHandler(RequestHandler):
    
    def initialize(self):
        cam = cv2.VideoCapture(0)
        for x in range(0, 30):
            self.tmp = cam.read()
        fname = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M.png")
        cv2.imwrite(fname, self.tmp)
        del(cam)

    def get(self, *args, **kwargs):
       self.set_header("Content-Type", "image/png")
       self.write(self.tmp)
