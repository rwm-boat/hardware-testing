# Simple demo of the LSM9DS0 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import time
import numpy
import board
import busio
# import digitalio # Used with SPI

import adafruit_lsm9ds0

# I2C connection:
i2c =(busio.I2C(board.SCL, board.SDA))
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)

#SPI connection:
# from digitalio import DigitalInOut, Direction
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# gcs = DigitalInOut(board.D5)
# xmcs = DigitalInOut(board.D6)
# sensor = adafruit_lsm9ds0.LSM9DS0_SPI(spi, xmcs, gcs)

# Main loop will read the acceleration, magnetometer, gyroscope, Temperature
# values every second and print them out.
while True:
    # Read acceleration, magnetometer, gyroscope, temperature.
    accel_x, accel_y, accel_z = sensor.acceleration
    mag_x, mag_y, mag_z = sensor.magnetic
    gyro_x, gyro_y, gyro_z = sensor.gyro
    temp = sensor.temperature
    compass = round(-(24 + numpy.degrees(numpy.arctan2(mag_x, mag_y))))
    if compass < 0:
        compass = 360 + compass

    # Print values.
   # print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(accel_x, accel_y, accel_z))
    #print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(mag_x, mag_y, mag_z))
    print("Heading: %s" %(compass))
   # print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
    #print('Temperature: {0:0.3f}C'.format(temp))
    # Delay for a second.
    time.sleep(0.25)
