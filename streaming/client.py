import sys, traceback, Ice
import Image
import numpy as np
import cv2
status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    base = ic.stringToProxy("ImageServer:tcp -p 10000 -h 192.168.9.2")
    im = Image.ImageProviderPrx.checkedCast(base).ice_twoway().ice_secure(False);
    udp = Image.ImageProviderPrx.uncheckedCast(im.ice_datagram());
    if not im:
        raise RuntimeError("Invalid proxy")

    while 1:
        imagen = im.getImageData()
        print imagen.width, imagen.height
        #print imagen.imageData
        img = np.frombuffer(imagen.imageData, dtype=np.uint8)
        img.shape = imagen.width, imagen.height, 3
        cv2.imshow('recibido',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
except:
    traceback.print_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)
