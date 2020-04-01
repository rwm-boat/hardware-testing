


import RPi.GPIO as GPIO
import numpy
import time
import json
#from mqtt_client.publisher import Publisher
#from mqtt_client.subscriber import Subscriber
#from threading import Thread
def on_count_up_command():
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        resistor_val = GPIO.setup(26,GPIO.IN)
        print(resistor_val)
    except Exception:
        print("LED FAILTURE")

on_count_up_command()
