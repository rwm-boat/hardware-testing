from gps3.agps3threaded import AGPS3mechanism
import time
import json
from mqtt_client.publisher import Publisher

agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default '()' 0.2 two tenths of a second

pubber = Publisher(client_id="gps-values")

def publish_gps_status():
    message = {
        'time' :  agps_thread.data_stream.time,
        'latitude' : agps_thread.data_stream.lat,
        'longitude' : agps_thread.data_stream.lon,
        'speed (m/s)' : agps_thread.data_stream.speed,
        'speed (kn)' : agps_thread.data_stream.speed * 1.943844,
        'course': agps_thread.data_stream.track
    }

    app_json = json.dumps(message)
    pubber.publish("/status/gps",app_json)
    time.sleep(0.1)

while True:  # All data is available via instantiated thread data stream attribute.
    publish_gps_status()



