import RPi.GPIO as GPIO
import time

class Locker() :
    def __init__(self) :
        self.motor = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) 
        GPIO.setup(self.motor, GPIO.OUT)
        self.p = GPIO.PWM(self.motor, 50) #purse
        self.p.start(0)
    
    #Servo
    def unlock(self):
        self.p.start(0)
        self.p.ChangeDutyCycle(9.2) #open
        time.sleep(1)
        self.p.stop()
        print("movmov")
        
    def lock(self):
        self.p.start(0)
        self.p.ChangeDutyCycle(4.0) #close
        time.sleep(1)
        self.p.stop()
        print("movmovmov")
        