from tkinter import *
import tkinter as tk
import tk_tools

import sys,os
import time
from mqtt_client.subscriber import Subscriber
from threading import Thread
import json

# global variables for plt.(Show)
mag_compass_reading = 0
int_compass_reading = 0
time_reading = 0
lat_reading = 0
lon_reading = 0
speed_reading =13
gps_heading_reading = 0
jet1_temp = 0
jet2_temp = 0
compartment_temp = 0
gps_distance = 0

jet1_current = 0 #starboard
jet2_current = 0 #port
pack_voltage = 0

#base for log files
_LOG_BASE = "log"

class Application(tk.Frame):
    #GUI

    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.updater()

    def create_widgets(self):
        self.pvgauge = tk_tools.Gauge(self, height = 200, width = 400,
                             min_value=0,
                             max_value=20,
                             label='Pack Voltage',
                             unit=' V',
                             divisions=30,
                             yellow=66,
                             red=70,
                             yellow_low=43,
                             red_low=40)
                             #bg='grey')
        self.pvgauge.grid(row=0, column=1, rowspan=3, sticky='news')
        self.FiNaEn = Entry(self)
        self.FiNaEn.grid(row=1, column=0)
        self.FiNaLa = Label(self, text="File name:")
        self.FiNaLa.grid(row=0, column=0, sticky='S')

        self.rs = tk_tools.RotaryScale(self, max_value=360, size=100, unit='km/h')
        self.rs.grid(row=0, column=4)

        self.StLog = Button(self, text="Start Log")
        self.StLog.grid(row=2,column=0, sticky='N')

    def update_pvgauge(self):
        global speed_reading

        self.pvgauge.set_value(speed_reading)

    def updater(self):
        self.update_pvgauge()
        self.after(100, self.updater)


# root = tk.Tk()
# root.title("RWM")

# pack_voltage_gauge = tk_tools.Gauge(root, height = 200, width = 400,
#                              min_value=0,
#                              max_value=20,
#                              label='Pack Voltage',
#                              unit=' V',
#                              divisions=30,
#                              yellow=66,
#                              red=70,
#                              yellow_low=43,
#                              red_low=40)
#                              #bg='grey')
# pack_voltage_gauge.grid(row=0, column=1, rowspan=3, sticky='news')


# def update_gauge():
#     global pack_voltage
#     global speed_reading
    
#     pack_voltage_gauge.set_value(speed_reading)
#     print("updating guage")
#     # update the gauges according to their value

#     #root.after(1000, update_gauge)

# def update_rs():
#     global gps_heading_reading
    
#     rs.set_value(gps_heading_reading)

#     # update the gauges according to their value

#     root.after(1000, update_rs)

def on_compass_received(client, userdata, message):
    global mag_compass_reading
    obj = json.loads(message.payload.decode('utf-8'))
    mag_compass_reading = obj['compass']

def on_internal_compass_received(client, userdata, message):
    global int_compass_reading
    obj = json.loads(message.payload.decode('utf-8'))
    int_compass_reading = obj['heading']

def on_gps_received(client, userdata, message):
    # create global variables for UI
    global time_reading
    global lat_reading
    global lon_reading
    global speed_reading
    global gps_heading_reading
    global gps_distance
    
    obj = json.loads(message.payload.decode('utf-8'))

    # parse json into global variablesspeed_reading,
    time_reading = obj["time"]
    lat_reading = obj['latitude']
    lon_reading = obj['longitude']
    speed_reading = obj["speed"]
    gps_heading_reading = obj["course"]
    gps_distance = obj['distance']

def on_adc_received(client, userdata, message):
    global jet1_current
    global jet2_current
    global pack_voltage

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_current = obj["jet1_amps"]
    jet2_current = obj["jet2_amps"]
    pack_voltage = obj['pack_voltage']
def on_temp_received(client, userdata, message):
    global jet1_temp
    global jet2_temp
    global compartment_temp

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_temp = obj["jet1_temp"]
    jet2_temp = obj["jet2_temp"]
    compartment_temp = obj["compartment_temp"]

# FiNaEn = Entry(root)
# FiNaEn.grid(row=1, column=0)
# FiNaLa = Label(root, text="File name:")
# FiNaLa.grid(row=0, column=0, sticky='S')

# rs = tk_tools.RotaryScale(root, max_value=360, size=100, unit='km/h')
# rs.grid(row=0, column=4)

# StLog = Button(root, text="Start Log")
# StLog.grid(row=2,column=0, sticky='N')


if __name__ == '__main__':

    try:
        print("try")
        default_subscriptions = {
            "/status/compass": on_compass_received,
            "/status/gps" : on_gps_received,
            "/status/adc" : on_adc_received,
            "/status/internal_compass" : on_internal_compass_received,
            "/status/temp" : on_temp_received
            #"/command/logging" : on_log_received
        }
        subber = Subscriber(client_id="teleGUI_live", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        thread.start()
        while True:
            root = tk.Tk()
            root.title("RWM")
            app = Application(root)
            root.mainloop()
            # print("while")
            # #root.mainloop()
            # root.update_gauge()
            # #root.after(1000, update_rs)
            # time.sleep(0.1)
            
            
            
        
    except KeyboardInterrupt:
        exit
#root.mainloop()