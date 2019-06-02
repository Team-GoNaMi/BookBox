from tkinter import *
import tkinter.font
import tkinter
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import cv2
import copy
import RPi.GPIO as GPIO
import requests
import json
import time
#from allGui import *
import os
from guigui import *
from qr_Recognize import *
#from qr_Recognize import *
#from locker import *
# Libraries Imported successfully

    
if __name__ == '__main__' :
    
    all_gui = GuiGui()
    all_gui.WELCOME_GUI()
    #all_gui.QR_GUI()
    print("closed welcome_gui")
    #qr = CodeRecognition()
    #success = qr.distinguish_user()
    
