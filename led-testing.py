import RPi.GPIO as GPIO
import time

while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(37,GPIO.OUT)
    GPIO.setup(35,GPIO.OUT)
    GPIO.setup(33,GPIO.OUT)
    print ("LED on")
    GPIO.output(37,GPIO.HIGH)
    GPIO.output(35,GPIO.HIGH)
    GPIO.output(33,GPIO.HIGH)
    time.sleep(3)
    print ("LED off")
    GPIO.output(37,GPIO.LOW)
    GPIO.output(35,GPIO.LOW)
    GPIO.output(33,GPIO.LOW)