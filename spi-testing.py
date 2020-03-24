import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0) # (bus, device)
spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)
spi.mode = 0b1
spi.lsbfirst = False
       
for x in range(10):
    msg = [0b11111111, 0b11111111]
    reply = spi.xfer2(msg)

    print("first frame: " + bin(reply[0]))
    print("second frame: " + bin(reply[1]))

    left_byte = reply[0]
    right_byte = reply[1]

    rotation = (((left_byte & 0xFF) << 8) | ( right_byte & 0xFF)) & ~0xC000

    print(rotation)
    print(bin(rotation))
    
    time.sleep(1)

