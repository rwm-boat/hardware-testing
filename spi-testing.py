import spidev
import time
from adafruit_motorkit import MotorKit

try:

    kit = MotorKit()

    spi = spidev.SpiDev()
    spi.open(0, 0) # (bus, device)
    spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)
    spi.mode = 0b1
    spi.lsbfirst = False

    kit.motor1.throttle = 0.25
        
    for x in range(1000):
        msg = [0b11111111, 0b11111111]
        reply = spi.xfer2(msg)

        left_byte = reply[0]
        right_byte = reply[1]

        raw_rotation = (((left_byte & 0xFF) << 8) | ( right_byte & 0xFF)) & ~0xC000
        adj_rotation = raw_rotation / (0x3FFF/360)

        print(adj_rotation)
        
        time.sleep(0.1)
        kit.motor1.throttle = 0

except KeyboardInterrupt:
    kit.motor1.throttle = 0

