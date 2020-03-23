import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0) # (bus, device)
spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)

    msg = [0b11111111, 0x00]
    reply = spi.xfer2(msg)

    print("first frame: " + bin(reply[0])
    print("second frame: " + bin(reply[1]))
       
for x in range(10):
    read_rawAngle()
    time.sleep(1)

