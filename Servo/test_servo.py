import RPi.GPIO as GPIO
import time
pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50) #purse

p.start(0)
#cnt=0
try:
    while True:

        p.ChangeDutyCycle(9.2)
        time.sleep(1)

        p.ChangeDutyCycle(4.0)
        time.sleep(1)

except KeyboardInterrupt:
    p.stop()

GPIO.cleanup()   