import spidev
import time
from adafruit_motorkit import MotorKit

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
    port_location = [260,295,330,5,40,75,110,150,186,222]
    cost = 0.033
    error = abs(read_angle() - (port_location[port])

    while (error > 4):
        error = abs(read_angle() - port_location[port])
        print("error: " + error)
        throttle = error * const
        print("throttle: " + throttle)
        kit.motor1.throttle(throttle)
    kit.motor1.throttle(0)
    
try:

    kit = MotorKit()

    spi = spidev.SpiDev()
    spi.open(0, 0) # (bus, device)
    spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)
    spi.mode = 0b1
    spi.lsbfirst = False

    port_select(1)

except KeyboardInterrupt:
    kit.motor1.throttle = 0

