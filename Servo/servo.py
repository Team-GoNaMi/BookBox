import RPi.GPIO as GPIO
import time
pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)

p.start(0) #?? move regardless of the value
try:
    p.ChangeDutyCycle(9) #90degree - go to middle(open)
    time.sleep(1)
    p.ChangeDutyCycle(4) #90degree -go to right(closed)
    time.sleep(1)
    
except KeyboardInterrupt:
    p.stop()
    
finally:
    GPIO.cleanup()
        