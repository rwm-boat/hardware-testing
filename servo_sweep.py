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

def setup():
    ESC.angle = 0
    DIR.angle = 90
    RB.angle = 0


def th_rq(mag):
    vel = abs(mag)
    vel = (vel*18)/10
    ESC.angle = vel
    print("ESC Velocity: " + vel)


th_rq(100)
time.sleep(2)
th_rq(0)

