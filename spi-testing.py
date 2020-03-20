import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0) # (bus, device)
spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)

def calcEvenParity(value):
    cnt = 0b0
    i = 0b0 
    
    for i in range(10):
        if(value & 0x1)
            cnt = cnt + 1
        value >>= 1
    return cnt & 0x1

def read_rawAngle():

# Raw Angle Adress 0x3FFF
# Read Frame: (Parity(MSB),EF(Error Flag), 14 bit adressed data)

angle_adress = 0x3FFF
command = 0b0100000000000000
command = command | registerAdress

command |= (calcEvenParity(command)<<15)

reply = spi.xfer2(msg)

print(reply)


