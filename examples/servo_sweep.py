from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

#Port Jet (Red Wires to Pi) JET2
PESC = kit.servo[0]
PDIR = kit.servo[2]
PRB = kit.servo[1]
 
#Starboard Jet (Black Wires to Pi) JET1
SESC = kit.servo[4]
SDIR = kit.servo[6]
SRB = kit.servo[5]

#------Tuining Variables
reverse_limit = 0.3

# ESC
PESC.actuation_range = 180 
PESC.set_pulse_width_range(930,2300) #correct microsecond range for Turnigy 70A ESC

SESC.actuation_range = 180 
SESC.set_pulse_width_range(930,2300) #correct microsecond range for Turnigy 70A ESC


# DIR
PDIR.actuation_range = 180
PDIR.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos

SDIR.actuation_range = 180
SDIR.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos

# RB
PRB.actuation_range = 180
PRB.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos

SRB.actuation_range = 180
SRB.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos

def setup():
    th_rq(1,0)
    dir_rq(1,0)
    rb_rq(1,1)
    th_rq(2,0)
    dir_rq(2,0)
    rb_rq(2,1)
    time.sleep(5)
    print("ESC ARMED")


def th_rq(jet,mag):

    if mag > 100:
        mag = 100
        print("Throttle limited to 100")

    if mag < -100:
        mag = -100
        print("Throttle limited to -100")

    vel = ((abs(mag))*18)/10

#---------------reverse bucket
    # if mag > 0:
    #     rb_rq(1)

    # if mag < 0:
    #     vel = vel*reverse_limit
    #     rb_rq(3)

#------------------------------
    if vel < 10 and vel > 0:
        vel = 10

    if vel > 180:
        vel = 180

    if jet == 1:
        SESC.angle = vel
    
    if jet == 2:
        PESC.angle = vel

    #ESC.angle = vel
    print(vel)


def rb_rq(jet,level): #not set values

    if level == 1: #down
        pos = 20

    if level == 2: #mid
        pos = 75

    if level == 3: #up
        pos = 100

    if jet == 1:
        SRB.angle = pos
    
    if jet == 2:
        PRB.angle = pos



def dir_rq(jet,angle): #range is -25 to 25 degrees
    
    if angle > 25:
        angle = 25
        print("Director limited to 25")

    if angle < -25:
        angle = -25
        print("Director limited to -25")

    servo_angle = 90 + angle

    if jet == 1:
        SDIR.angle = servo_angle
    
    if jet == 2:
        PDIR.angle = servo_angle

    #DIR.angle = servo_angle


setup()
#th_rq(1,10)
rb_rq(1,2)
#dir_rq(1,-20)
#th_rq(2,10)
rb_rq(2,2)
#dir_rq(2,-20)


