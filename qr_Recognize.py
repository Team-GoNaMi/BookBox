from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import cv2
import copy
import time
from connect_database import *

# global isUserSeller #seller: true, buyer:false

class CodeRecognition() :
    
    #QR/Barcode   
    def recognize_code(self):

        ap = argparse.ArgumentParser()
        ap.add_argument("-o", "--output", type = str, default = "barcodes.csv", help = "path to output CSV file containing barcodes")
        args = vars(ap.parse_args())
        print("[INFO] starting video stream...")

        csv = open(args["output"], "w")
        found = set()

        #cap = VideoStream(src=0).start()
        cap = cv2.VideoCapture(0)
        cap.release()
        cap = cv2.VideoCapture(0)
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
        #cvReleaseCapture(cap)

        print("[INFO] cleaning up...")
        csv.close()
        cv2.waitKey(27)
        cv2.destroyAllWindows()
        #cap.stop()
        #print(barcode_data)
        
        
    def distinguish_user(self) :
        # DB Connection
        if (self.code_data != "") :
            db_connection = ConnectDB()
            self.qr_data = self.code_data.split("$$$")
        
            print(self.qr_data)

        
            if(len(self.qr_data) == 3):
                self.isUserSeller = True
                self.db_data = db_connection.check_seller(self.qr_data[1], self.qr_data[2])
                
                if (self.db_data['success']):
                    self.success = True
                    self.box_id = self.db_data['box_id']
            
                else:
                    self.success = False
                    self.box_id = "NotFound"
    
                
                #self.success, self.box_id = db_connection.check_seller(self.qr_data[1], self.qr_data[2])
                print("@@seller")
                print(self.success)
                print(self.box_id)
        
            elif(len(self.qr_data) == 2):
                self.isUserSeller = False
                
                self.db_data = db_connection.check_buyer(self.qr_data[0], self.qr_data[1])
                
                if (self.db_data['success']):
                    self.success = True
                    self.box_id = self.db_data['box_id']
                
                else:
                    self.success = False
                    self.box_id = "NotFound"
                
                
                #self.success, self.box_id = db_connection.check_seller(self.qr_data[0], self.qr_data[1])
                print("@@buyer")
                print(self.success)
                print(self.box_id)
    
    def gogoSing(self) :
        self.recognize_code()
        self.distinguish_user()
    
    def get_success(self) :
        return self.success
    
    def get_box_id(self) :
        return self.box_id
    
    def get_barcode(self) :
        return self.qr_data[0]
    
    def isSeller(self) :
        return self.isUserSeller
    
    def get_register_id(self) :
        if self.isUserSeller :
            return self.qr_data[1]
        else :
            return self.qr_data[0]