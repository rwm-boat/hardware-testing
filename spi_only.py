import spidev
import time

spi = spidev.SpiDev()

def read_angle():
    msg = [0b11111111, 0b11111111]
    reply = spi.xfer2(msg)
    
#    msg = [0b00000001, 0b00000001]
#    reply2 = spi.xfer2(msg)

    left_byte = reply[0]
    right_byte = reply[1]

    raw_rotation = (((left_byte & 0xFF) << 8) | ( right_byte & 0xFF)) & ~0xC000
    adj_rotation = raw_rotation / (0x3FFF/360)

    print("raw angle: " + str(adj_rotation))
    spi.close()
    return adj_rotation

while(True):
    spi.open(0, 0)
    spi.max_speed_hz = 100000
    spi.mode = 0b1
    spi.lsbfirst = False
    read_angle()
    time.sleep(0.01)
