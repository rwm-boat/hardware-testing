from gps3.agps3threaded import AGPS3mechanism
import time
import json
from mqtt_client.publisher import Publisher

agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default '()' 0.2 two tenths of a second

pubber = Publisher(client_id="gps-values")

while True:  # All data is available via instantiated thread data stream attribute.
    # line #140-ff of /usr/local/lib/python3.5/dist-packages/gps3/agps.py
    # print('---------------------')
    # print(                   agps_thread.data_stream.time)
    # print('Lat:{}   '.format(agps_thread.data_stream.lat))
    # print('Lon:{}   '.format(agps_thread.data_stream.lon))
    # print('Speed:{} '.format(agps_thread.data_stream.speed))
    # print('Course:{}'.format(agps_thread.data_stream.track))
    # print('---------------------')

    message = {
        "time" :  agps_thread.data_stream.time,
        "latitude" : agps_thread.data_stream.lat,
        "longitude" : agps_thread.data_stream.lon
    }

    app_json = json.dump(message)
    print(app_json)
    time.sleep(1) # Sleep, or do other things for as long as you like.