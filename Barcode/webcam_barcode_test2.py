from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type = str, default = "barcodes.csv", help = "path to output CSV file containing barcodes")
args = vars(ap.parse_args())

print("[INFO] starting video stream...")

csv = open(args["output"], "w")
found = set()

cap = cv2.VideoCapture(0)
#time.sleep(2.0)

while cap.isOpened():
    ret, img = cap.read()
    
    if ret :
        img = cv2.flip(img, 1)
        barcodes = pyzbar.decode(img)

        for barcode in barcodes :
            (x, y, w, h) = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(img, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if barcodeData not in found:
                csv.write("{},{}\n".format(datetime.datetime.now(),barcodeData))
                csv.flush()
                found.add(barcodeData)

        cv2.imshow('camera-0', img)
        key = cv2.waitKey(1) & 0xFF
 
        if key == ord("q"):
            break

    else:
        print('no camera')
        break

cap.release()

print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
cap.stop() 