import time
import numpy
import board
import busio
import json
from mqtt_client.publisher import Publisher

import adafruit_lsm9ds0

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
pubber = Publisher(client_id="compass-values")

def publish_compas_status():
    mag_x, mag_y, mag_z = sensor.magnetic
    temp = sensor.temperature
    compass = round(-(24 + numpy.degrees(numpy.arctan2(mag_x, mag_y))))
    if compass < 0:
        compass = 360 + compass
    message = {
        'temp' : temp,
        'compass': compass,
    }
    print(json.dumps(message))
    app_json = json.dumps(message)
    pubber.publish("/status/compass",app_json)
    


# Main loop will read the acceleration, magnetometer, gyroscope, Temperature
# values every second and print them out.
while True:
    # Read acceleration, magnetometer, gyroscope, temperature.
    # accel_x, accel_y, accel_z = sensor.acceleration
    # mag_x, mag_y, mag_z = sensor.magnetic
    # gyro_x, gyro_y, gyro_z = sensor.gyro
    # temp = sensor.temperature
    # compass = round(-(24 + numpy.degrees(numpy.arctan2(mag_x, mag_y))))
    # if compass < 0:
    #     compass = 360 + compass
    publish_compas_status()
    time.sleep(0.25)
