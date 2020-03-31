import spidev
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()
spi = spidev.SpiDev()
iError = 0
lastError = 0
def read_angle():
    msg = [0b11111111, 0b11111111]
    reply = spi.xfer2(msg)

    left_byte = reply[0]
    right_byte = reply[1]

    raw_rotation = (((left_byte & 0xFF) << 8) | ( right_byte & 0xFF)) & ~0xC000
    adj_rotation = raw_rotation / (0x3FFF/360)

    print(adj_rotation)

    return adj_rotation

def port_select(port):

    # [PURGE,ONE,...,NINE]
    port_location = [97.2,133.3,170.6,203.7,244.3,277.5,314.5,351.8,24.7,64.6]
    Kp = 1/100
    Ki = 1/1500
    Kd = 1/1000
    error = (read_angle() - (port_location[port]))
    global iError
    iError = iError + error
    global lastError
    while error > .1 or error < -0.1:
        error = (read_angle() - port_location[port])
        print("error: " + str(error))
        iError = iError + error
        throttle = (error * Kp) + (iError * Ki) + (Kd * (error - lastError))
        print("Kp error:" + str(error * Kp))
        print("Ki error:" + str(iError * Ki))
        print("Kd error:" + str(Kd * (error - lastError)))
        print("Throttle:" + str(throttle))
        if error == 0: Ki = 0
        lastError = error
        #print("throttle: " + str(throttle))
        if throttle > 1: throttle = .95
        if throttle < -1: throttle = -.95
        print(str(throttle))
        kit.motor1.throttle = throttle
    kit.motor1.throttle = 0
    
try:
    
    spi.open(0, 0) # (bus, device)
    spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)
    spi.mode = 0b1
    spi.lsbfirst = False

    port_select(3)

except KeyboardInterrupt:
    kit.motor1.throttle = 0

