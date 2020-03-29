import spidev
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()
spi = spidev.SpiDev()

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
    port_location = [99,134,172,208,250,285,328,359,27,65]
    const = 1/20
    error = abs(read_angle() - (port_location[port]))

    while error > 1:
        error = abs(read_angle() - port_location[port])
        print("error: " + str(error))
        throttle = error * const
        print("throttle: " + str(throttle))
        if throttle > 1: throttle = 1
        kit.motor1.throttle = throttle
    kit.motor1.throttle = 0
    
try:
    
    spi.open(0, 0) # (bus, device)
    spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)
    spi.mode = 0b1
    spi.lsbfirst = False

    port_select(5)

except KeyboardInterrupt:
    kit.motor1.throttle = 0

