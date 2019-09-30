import RPi.GPIO as GPIO
import time

try:
    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(26,GPIO.OUT)
        GPIO.setup(19,GPIO.OUT)
        GPIO.setup(13,GPIO.OUT)
        print ("LED on")
        GPIO.output(26,GPIO.HIGH)
        GPIO.output(19,GPIO.HIGH)
        GPIO.output(13,GPIO.HIGH)
        time.sleep(2)
        print ("LED off")
        GPIO.output(26,GPIO.LOW)
        GPIO.output(19,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        time.sleep(2)
except KeyboardInterrupt:
    print("ended")


