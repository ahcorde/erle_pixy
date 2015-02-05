import sys, traceback, Ice
import Image
import numpy as np
import cv2

import threading, time
from datetime import datetime

time_cycle = 80;

class MiThread(threading.Thread):  
    def __init__(self, ):
        self.cap = cv2.VideoCapture(0)
        #        ret = self.cap.set(3,180)
        #ret = self.cap.set(4,120)
        print("Constructor thread")
        self.stop = 0
        self.lock = threading.Lock()  
        threading.Thread.__init__(self)  
 
    def run(self):  
        while(True):
            
            start_time = datetime.now()

            self.lock.acquire();
            ret, self.img = self.cap.read()
            self.lock.release();
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            finish_Time = datetime.now()
            
            dt = finish_Time - start_time
            ms=(dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            if(ms < time_cycle):
                time.sleep((time_cycle-ms) / 1000.0);
            if (self.stop==1):
                break;

    def getImage(self):
        self.lock.acquire();
        imagen_result = self.img.copy()
        self.lock.release();
        return imagen_result

    def setStop(self):
        self.stop =1;

class ImageProvider(Image.ImageProvider):
    def __init__(self, t):
        self.t = t

    def getImageData(self, current=None):
        #ret, img = cap.read()
        img = self.t.getImage()
        data = Image.ImageDescription()
        data.width = img.shape[0]
        data.height = img.shape[1]
        data.imageData = img
        return data

if __name__ == "__main__":

    status = 0
    ic = None
    t2 = MiThread()
try:

    t2.start()

    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints("ImageServer", "tcp -p 10000:udp -p 10000")
    object = ImageProvider(t2)
    adapter.add(object, ic.stringToIdentity("ImageServer"))
    adapter.activate()
    ic.waitForShutdown()
except:
    traceback.print_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
        exit()
    except:
        traceback.print_exc()
        status = 1
        t2.setStop()
        
sys.exit(status)

