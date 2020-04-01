import RPi.GPIO as GPIO
#from mqtt_client.publisher import Publisher
#from mqtt_client.subscriber import Subscriber
#from threading import Thread
def on_count_up_command():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26,GPIO.IN)
    i = GPIO.input(26)
    count = 0
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26,GPIO.IN)
        i = GPIO.input(26)
        print(count)
        print("I:" + i)
    except:
        print("hello")

on_count_up_command()
