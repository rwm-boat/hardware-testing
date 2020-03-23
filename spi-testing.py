import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0) # (bus, device)
spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)

def calcEvenParity(value):
    cnt = 0b0
    i = 0b0 
    
    for i in range(10):
        if value & 0x1:
            cnt = cnt + 1
        value >>= 1
    return cnt & 0x1

def read_rawAngle():

    # Raw Angle Adress 0x3FFF
    # Read Frame: (Parity(MSB),EF(Error Flag), 14 bit adressed data)

    angle_adress = 0x3FFF
    command = 0b0100000000000000
    command = command | angle_adress

    command |= (calcEvenParity(command)<<15)
    print("sent message: " + bin(command))
    msg = [command, 0x3FFF]
    reply = spi.xfer2(msg)

    print("response: " + bin(reply[0]& ~0xC000))
    

for x in range(10):
    read_rawAngle()
    time.sleep(1)

