from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import cv2
import copy
import time
from connect_database import *


class BarRecognition() :
    
    #QR/Barcode   
    def recognize_bar(self):

        ap = argparse.ArgumentParser()
        ap.add_argument("-o", "--output", type = str, default = "barcodes.csv", help = "path to output CSV file containing barcodes")
        args = vars(ap.parse_args())
        print("[INFO] starting video stream...")

        csv = open(args["output"], "w")
        found = set()

        #cap = VideoStream(src=0).start()
        cap = cv2.VideoCapture(1)
        time.sleep(2.0)

        found = False
        barcode_data = ""

        while cap.isOpened():
            ret, img = cap.read()
    
            if ret :
                #img = cv2.flip(img, 1)
                barcodes = pyzbar.decode(img)

                for barcode in barcodes :
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
            
                    barcode_data = copy.deepcopy(barcodeData)

                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(img, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
                    time.sleep(1)
            
                    if barcode_data != "" :
                        # 클래스 변수로 저장
                        self.code_data = copy.deepcopy(barcode_data)
                        found = True
                        break

                cv2.imshow('camera-0', img)
                key = cv2.waitKey(1) & 0xFF
         
                if found :
                    break
        
                if key == ord("q"):
                    break

            else:
                print('no camera')
                break

        cap.release()

        print("[INFO] cleaning up...")
        csv.close()
        cv2.waitKey(27)
        cv2.destroyAllWindows()
        #cap.stop()
        #print(barcode_data)
        
    
    def gogoRing(self) :
        self.recognize_bar()
    
#    def get_box_id(self) :
#        return self.box_id
    
    def get_barcode(self) :
        return self.code_data
