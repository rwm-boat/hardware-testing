


import RPi.GPIO as GPIO
import numpy
import time
import json
#from mqtt_client.publisher import Publisher
#from mqtt_client.subscriber import Subscriber
#from threading import Thread
def on_count_up_command():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26,GPIO.IN)
    i = GPIO.input(26)
    count = 0
    try:
        while (1):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(26,GPIO.IN)
            i = GPIO.input(26)
            print(i)
            if (i):
                print("i = 1")
            else:
                while (not i):
                    count = count
                count = count + 1
            print (count)
            
    except Exception:
        print("Light Resistor FAILURE")

on_count_up_command()
