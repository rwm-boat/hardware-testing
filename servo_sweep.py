from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
ESC = kit.servo[0]
DIR = kit.servo[1]
RB = kit.servo[2]

# ESC
ESC.actuation_range = 180 #for DS3218mg servos
ESC.set_pulse_width_range(500,2400) #correct microsecond range for DS3218mg servos

# DIR
DIR.actuation_range = 180
DIR.set_pulse_width_range(500, 2400)

# RB
RB.actuation_range = 180
RB.set_pulse_width_range(500, 2400)

ESC.angle = 0
DIR.angle = 0
RB.angle = 0

time.sleep(3)

ESC.angle = 180
DIR.angle = 180
RB.angle = 180

time.sleep(3)


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

# for x in range(180,0):
#    kit.servo[0].angle = x
#    time.sleep(.1)
