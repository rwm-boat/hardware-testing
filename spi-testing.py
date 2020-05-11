import spidev
import time
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
from simple_pid import PID

kit = MotorKit()
spi = spidev.SpiDev()
iError = 0

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)


def read_angle():
    msg = [0b11111111, 0b11111111]
    reply = spi.xfer2(msg)

    left_byte = reply[0]
    right_byte = reply[1]

    raw_rotation = (((left_byte & 0xFF) << 8) | ( right_byte & 0xFF)) & ~0xC000
    adj_rotation = raw_rotation / (0x3FFF/360)

    #print("raw angle: " + str(adj_rotation))

    return adj_rotation

def port_select(port):

    # [PURGE,ONE,...,NINE]
    port_location = [97,134,172,208,250,285,328,359,27,65]
    error = abs(read_angle() - (port_location[port]))
    #pid = PID(1, 0.1, 0.05, setpoint = 1)
    # global iError
    # iError = iError + error
    # Kp = 1/10
    # Ki = 1/50
    # while error > .5:
    #     error = abs(read_angle() - port_location[port])
    #     print("error: " + str(error))
    #     throttle = (error * Kp) 
    #     #+ (iError * Ki)
    #     print("throttle: " + str(throttle))
    #     if throttle > 1: throttle = 1
    #     kit.motor1.throttle = throttle
    # kit.motor1.throttle = 0
    pid = PID(1/100, 0, 0, setpoint=1) 
    pid.sample_time = 0.01
    pid.output_limits = (-1,1)

    while error > .5 or error < -0.5:
        angle = read_angle()
        error = angle - port_location[port]
        
        output = pid(angle)
        pid.setpoint = port_location[port]
        print("setpoint : " + str(port_location[port]))
        print("raw angle: " + str(angle))
        print("throttle : " + str(output))
        kit.motor1.throttle = output

        time.sleep(0.01)
       
    kit.motor1.throttle = 0

def fwd_pump():
   GPIO.output(23,GPIO.LOW)
   GPIO.output(24,GPIO.HIGH)
def rev_pump():
   GPIO.output(24,GPIO.HIGH)
   GPIO.output(23,GPIO.LOW)
def stop_pump():
    GPIO.output(23,GPIO.LOW)
    GPIO.output(24,GPIO.LOW)

try:
    spi.open(0, 0) # (bus, device)
    spi.max_speed_hz = 1000000 # 1MHz clock (AMS accepts up to 10MHz)
    spi.mode = 0b1
    spi.lsbfirst = False

    port_select(0)
    time.sleep(5)
    port_select(5)
#    fwd_pump()
 #   time.sleep(2)
  #  stop_pump()
   # port_select(2)
    #fwd_pump()
    #time.sleep(2)
    #stop_pump()

except KeyboardInterrupt:
    kit.motor1.throttle = 0
    stop_pump()

