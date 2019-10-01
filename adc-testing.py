import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)

pubber = Publisher(client_id="adc-values")

def publish_compas_status():
    message = {
        'value' : chan.value,
        'voltage': chan.voltage,
    }

    app_json = json.dumps(message)
    pubber.publish("/status/adc",app_json)
    

try:
    while True:
        publish_adc_status()
        time.sleep(1)
except KeyboardInterrupt:
    print("ended")
