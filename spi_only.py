import spidev
import time

def read_angle():
    msg = [0b11111111, 0b11111111]
    reply = spi.xfer2(msg)

    left_byte = reply[0]
    right_byte = reply[1]

    raw_rotation = (((left_byte & 0xFF) << 8) | ( right_byte & 0xFF)) & ~0xC000
    adj_rotation = raw_rotation / (0x3FFF/360)

    print("raw angle: " + str(adj_rotation))

    return adj_rotation