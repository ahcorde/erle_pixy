import sys, traceback, Ice
import Image
import numpy as np
import cv2

Ice.loadSlice('Image.ice')


class Client(Ice.Application):
    def run(self, args):
        if len(args) > 1:
            print(self.appName() + ": too many arguments")
            return 1
        
        twoway = Image.ImageProviderPrx.checkedCast(self.communicator().propertyToProxy('ImageServer.Proxy'))
        if not twoway:
            print(args[0] + ": invalid proxy")
            return 1
        print twoway.ice_isDatagram()

        udp = Image.ImageProviderPrx.uncheckedCast(twoway.ice_batchDatagram());
        if not udp:
            raise RuntimeError("Invalid proxy")

        while 1:
            imagen = twoway.getImageData()
            print imagen.width, imagen.height
            #print imagen.imageData
            img = np.frombuffer(imagen.imageData, dtype=np.uint8)
            decimg=cv2.imdecode(img,1)
            decimg.shape = imagen.width, imagen.height, 3
            cv2.imshow('recibido',decimg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cv2.destroyAllWindows()

app = Client()
sys.exit(app.main(sys.argv, "config.client"))
