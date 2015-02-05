#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2014 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************



import sys, traceback, Ice
import Image
import numpy as np
import cv2

import threading, time
from datetime import datetime

time_cycle = 80;

Ice.loadSlice('Image.ice')
Ice.updateModules()

class MiThread(threading.Thread):
    def __init__(self, ):
        self.cap = cv2.VideoCapture(0)
        ret, self.img = self.cap.read()
        #ret = self.cap.set(3,640)
        #ret = self.cap.set(4,480)
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
        ret, buf = cv2.imencode(".jpg", img, [1, 35]);
        data.sizeCompress = buf.shape[0]
        data.imageData = buf
        return data

        current.adapter.getCommunicator().shutdown()

class Server(Ice.Application):
    def run(self, args):
        if len(args) > 1:
            print(self.appName() + ": too many arguments")
            return 1
        
        t2 = MiThread()
        t2.start();

        object = ImageProvider(t2)

        adapter = self.communicator().createObjectAdapter("ImageServer")
        adapter.add(object, self.communicator().stringToIdentity("ImageServer"))
        adapter.activate()
        self.communicator().waitForShutdown()
        return 0

sys.stdout.flush()
app = Server()
sys.exit(app.main(sys.argv, "config.server"))
