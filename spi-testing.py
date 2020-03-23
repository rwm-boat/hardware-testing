import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0) # (bus, device)
spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)


       
for x in range(10):
    msg = [0b11111111, 0b11111111]
    reply = spi.xfer2(msg)

    print("first frame: " + bin(reply[0]))
    print("second frame: " + bin(reply[1]))
    
    time.sleep(1)

