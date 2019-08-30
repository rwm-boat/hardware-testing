from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

kit.servo[0].actuation_range = 180
kit.servo[0].set_pulse_width_range(1000,2000)


for x in range(180):
   kit.servo[0].angle = x
   time.sleep(.1)

for x in range(180,0):
   kit.servo[0].angle = x
   time.sleep(.1)
