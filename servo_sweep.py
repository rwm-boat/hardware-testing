from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

ESC = kit.servo[0]
DIR = kit.servo[1]
RB = kit.servo[2]

#------Tuining Variables
reverse_limit = 0.3

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
    th_rq(0)
    dir_rq(0)
    rb_rq(1)
    time.sleep(5)
    print("ESC ARMED")


def th_rq(mag):

    if mag > 100:
        mag = 100
        print("Throttle limited to 100")

    if mag < -100:
        mag = -100
        print("Throttle limited to -100")

    vel = ((abs(mag))*18)/10

#---------------reverse bucket
    if mag > 0:
        rb_rq(1)

    if mag < 0:
        vel = vel*reverse_limit
        rb_rq(3)

#------------------------------
    if vel < 10 and vel > 0:
        vel = 10

    if vel > 180:
        vel = 180

    ESC.angle = vel
    print(vel)


def rb_rq(level): #not set values

    if level == 1: #up
        RB.angle = 0

    if level == 2: #mid
        RB.angle = 50

    if level == 3: #down
        RB.angle = 100


def dir_rq(angle): #range is -25 to 25 degrees
    
    if angle > 25:
        angle = 25
        print("Director limited to 25")

    if angle < -25:
        angle = -25
        print("Director limited to -25")

    servo_angle = 90 + angle

    DIR.angle = servo_angle


setup()
th_rq(30)
time.sleep(2)
th_rq(-30)
time.sleep(3)
th_rq(0)
