import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup (23,GPIO.OUT)
GPIO.setup (24,GPIO.OUT)

GPIO.output(23,GPIO.LOW)
GPIO.output(24,GPIO.HIGH)

time.sleep(3)

GPIO.output(23,GPIO.HIGH)
GPIO.output(24,GPIO.LOW)

time.sleep(3)

GPIO.output(23,GPIO.LOW)
GPIO.output(24,GPIO.LOW)

GPIO.cleanup()
