from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tk_tools
import math
from application import Application
import sys,os
import time
from mqtt_client.subscriber import Subscriber
from threading import Thread
import json
import math

#base for log files
_LOG_BASE = "log"

def on_compass_received(client, userdata, message):

    obj = json.loads(message.payload.decode('utf-8'))
    mag_compass_reading = obj['compass']

    try:
        app.rs.set_value(round(mag_compass_reading, 2))
        app.Mag_Compass_Dig.set_value(str(round(mag_compass_reading, 2)))
    except:
        pass

def on_gps_received(client, userdata, message):
        
    obj = json.loads(message.payload.decode('utf-8'))
    time_reading = obj["time"]
    lat_reading = obj['latitude']
    lon_reading = obj['longitude']
    speed_reading = obj["speed"]
    gps_heading_reading = obj["course"]
    gps_distance = obj['distance']

    try:
        app.spdgauge.set_value(round(speed_reading,2))
        app.Latitude_Dig.set_value(str(round(lat_reading, 7)))
        app.Longitude_Dig.set_value(str(round(lon_reading, 7)))
        app.GPS_Speed_Dig.set_value(str(round(speed_reading, 2)))
        app.GPS_Compass_Dig.set_value(str(round(gps_heading_reading, 2)))
        app.GPS_Distance_Dig.set_value(str(round(gps_distance, 5)))
    except:
        pass

def on_adc_received(client, userdata, message):

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_current = obj["jet1_amps"]
    jet2_current = obj["jet2_amps"]
    pack_voltage = obj['pack_voltage']

    try:
        app.pvgauge.set_value(pack_voltage)
        app.Port_Jet_Current_Dig.set_value(str(round(jet2_current, 2)))
        app.Starboard_Jet_Current_Dig.set_value(str(round(jet1_current, 2)))
        
        delta = abs(jet1_current-jet2_current)
        if delta > 10: app.Delta_Status_Led.to_red(on=False)
        app.Delta_Jet_Current_Dig.set_value(str(round(delta, 2)))
    except:
        pass

def on_temp_received(client, userdata, message):
    
    obj = json.loads(message.payload.decode('utf-8'))
    jet1_temp = obj["jet1_temp"]
    jet2_temp = obj["jet2_temp"]
    compartment_temp = obj["compartment_temp"]

def on_vector_received(client, userdata, message):
    
    obj = json.loads(message.payload.decode('utf-8'))
    target_heading = obj["heading"]
    magnitude = obj["magnitude"]

    try:
        app.Target_Heading_Dig.set_value(str(round(target_heading, 2)))
    except:
        pass

if __name__ == '__main__':

    try:
      
        default_subscriptions = {
            "/status/compass": on_compass_received,
            "/status/gps" : on_gps_received,
            "/status/adc" : on_adc_received,
            "/status/temp" : on_temp_received,
            "/status/vector" : on_vector_received,
            #"/command/logging" : on_log_received
        }
        subber = Subscriber(client_id="teleGUI_live", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        thread.start()

        root = tk.Tk()
        root.title("RWM")
        app = Application(root)
        root.mainloop()
                                     
    except KeyboardInterrupt:
        exit()
