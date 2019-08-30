from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

ESC = kit.servo[0]
DIR = kit.servo[1]
RB = kit.servo[2]

# ESC
ESC.actuation_range = 180 
ESC.set_pulse_width_range(930,2300) #correct microsecond range for Turnigy 70A ESC

# DIR
DIR.actuation_range = 180
DIR.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos

# RB
RB.actuation_range = 180
RB.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos



ESC.angle = 0
DIR.angle = 0
RB.angle = 0

time.sleep(3)

DIR.angle = 180
RB.angle = 180

<<<<<<< HEAD
ESC.angle = 10
time.sleep(2)
ESC.angle = 0
=======
time.sleep(3)

ESC.angle = 30
time.sleep(1)
ESC.angle = 0


#kit.servo[0].angle = 90
#time.sleep(.25)
#kit.servo[0].angle = 180
#time.sleep(.25)
#kit.servo[0].angle = 90
#time.sleep(.25)
#kit.servo[0].angle = 0
#time.sleep(.25)

# for x in range(180):
#    kit.servo[0].angle = x
#    time.sleep(.1)
>>>>>>> e227014dd256811bf8e6b44dcf3f17002c081c77

