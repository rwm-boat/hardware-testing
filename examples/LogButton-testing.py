import RPi.GPIO as GPIO
import time

try:
    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        i = GPIO.input(26)
        if i:
            print("LED on")
            
        else: print("LED off")
except KeyboardInterrupt:
    print("ended")

