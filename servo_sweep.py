from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

kit.servo[0].actuation_range = 180 #for DS3218mg servos
kit.servo[0].set_pulse_width_range(500,2400) #correct microsecond range for DS3218mg servos


kit.servo[0].angle = 180
time.sleep(5)

kit.servo[0].angle = 0
time.sleep(5)

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
