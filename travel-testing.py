


import RPi.GPIO as GPIO

# #from mqtt_client.publisher import Publisher
# #from mqtt_client.subscriber import Subscriber
# #from threading import Thread
# def on_count_up_command():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(26,GPIO.IN)
#     i = GPIO.input(26)
#     count = 0
#     try:
#         while (1):
#             GPIO.setmode(GPIO.BCM)
#             GPIO.setup(26,GPIO.IN)
#             i = GPIO.input(26)
#             print(i)
#             if (i):
#                 print("i = 1")
#             else:
#                 while (not i):
#                     count = count
#                 count = count + 1
#             print (count)

#     except Exception:
#         print("Light Resistor FAILURE")

# on_count_up_command()

'''a very simple idiom for a state machine'''


from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)
i = GPIO.input(26)
count = 0
# Each of the state functions below performs some action and then implements
# logic to choose next state.  Each state function returns the next state.

def stateClear():
    i = GPIO.input(26)
    print ("stateClear")
    # delay and decision path to simulate some application logic
    sleep(.5)
    global count
    count = count
    if not i:
        return stateClear
    else:
        return stateDark

def stateDark():
    i = GPIO.input(26)
    print ("stateDark")
    # delay and decision path to simulate some application logic
    sleep(.5)
    global count
    
    if i:
        count = count + 1
        return stateClear
    else:
        return stateDark
state=stateClear    # initial state
while state: state=state()  # launch state machine
print ("Done with states")