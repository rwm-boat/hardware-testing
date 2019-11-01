from tkinter import *
import tkinter as tk
import tk_tools
import math


import sys,os
import time
from mqtt_client.subscriber import Subscriber
from threading import Thread
import json
import math

# global variables

mag_compass_reading = 0
int_compass_reading = 0
time_reading = 0
lat_reading = 0
lon_reading = 0
speed_reading = 0
gps_heading_reading = 0
jet1_temp = 0
jet2_temp = 0
compartment_temp = 0
gps_distance = 0

jet1_current = 0 #starboard
jet2_current = 0 #port
pack_voltage = 0

target_heading = 0
magnitude = 0

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


        # Pack Voltage Gauge
        self.pvgauge = tk_tools.Gauge(self, height = 200, width = 400,
                             min_value=10,
                             max_value=20,
                             label='Pack Voltage',
                             unit=' V',
                             divisions=30,
                             yellow=66,
                             red=70,
                             yellow_low=43,
                             red_low=40)
                             #bg='grey')
        self.pvgauge.grid(row=0, column=5, rowspan=3, columnspan=3, sticky='news')
        # Speed Gauge
        self.spdgauge = tk_tools.Gauge(self, height = 200, width = 400,
                             min_value=0,
                             max_value=20,
                             label='Speed',
                             unit=' (kn)',
                             divisions=20,
                             yellow=50,
                             red=70)
                             #bg='grey')
        self.spdgauge.grid(row=0, column=2, rowspan=3, columnspan=3, sticky='news')
        
        #File Name Entry Box
        self.FiNaEn = Entry(self)
        self.FiNaEn.grid(row=1, column=0)
        #File name Label
        self.FiNaLa = Label(self, text="File name:")
        self.FiNaLa.grid(row=0, column=0, sticky='S')
        

        
        
        #Value Labels, Digits
        self.Mag_Compass_Label = Label(self, text="Mag Compass:")
        self.Mag_Compass_Label.grid(row=3, column=0, sticky='E')
        
        self.Mag_Compass_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.Mag_Compass_Dig.grid(row=3, column=1, sticky='W', pady=4, ipady=2)
        
        self.Target_Heading_Label = Label(self, text="Target Heading:")
        self.Target_Heading_Label.grid(row=4, column=0, sticky='E')

        self.Target_Heading_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.Target_Heading_Dig.grid(row=4, column=1, sticky='W', pady=4, ipady=2)
        
        self.GPS_Compass_Label = Label(self, text="GPS Compass:")
        self.GPS_Compass_Label.grid(row=5, column=0, sticky='E')

        self.GPS_Compass_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.GPS_Compass_Dig.grid(row=5, column=1, sticky='W', pady=4, ipady=2)

        # self.GPS_Time_Label = Label(self, text="GPS Time:")
        # self.GPS_Time_Label.grid(row=6, column=0, sticky='E')

        # self.GPS_Time_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        # self.GPS_Time_Dig.grid(row=6, column=1, sticky='w')

        self.Latitude_Label = Label(self, text="Latitude:")
        self.Latitude_Label.grid(row=7, column=0, sticky='E')

        self.Latitude_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.Latitude_Dig.grid(row=7, column=1, sticky='w', pady=4, ipady=2)

        self.Longitude_Label = Label(self, text="Longitude:")
        self.Longitude_Label.grid(row=8, column=0, sticky='E')

        self.Longitude_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.Longitude_Dig.grid(row=8, column=1, sticky='w', pady=4, ipady=2)

        self.GPS_Speed_Label = Label(self, text="GPS Speed (kn):")
        self.GPS_Speed_Label.grid(row=9, column=0, sticky='E')

        self.GPS_Speed_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.GPS_Speed_Dig.grid(row=9, column=1, sticky='w', pady=4, ipady=2)

        self.GPS_Distance_Label = Label(self, text="GPS Distance:")
        self.GPS_Distance_Label.grid(row=10, column=0, sticky='E')

        self.GPS_Distance_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.GPS_Distance_Dig.grid(row=10, column=1, sticky='w', pady=4, ipady=2)


        #Jets Labels and Digits
        self.Port_Jet_Current_Label = Label(self, text="Port Jet Current:")
        self.Port_Jet_Current_Label.grid(row=3, column=2, sticky='NESW')

        self.Port_Jet_Current_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.Port_Jet_Current_Dig.grid(row=4, column=2, sticky='NEWS', pady=4, ipady=2, padx=4, ipadx=2)
        
        self.Delta_Jet_Current_Label = Label(self, text="Jet Current Delta:")
        self.Delta_Jet_Current_Label.grid(row=3, column=3, sticky='NESW')

        self.Delta_Jet_Current_Dig = tk_tools.SevenSegmentDigits(self, digits=5, background='black', digit_color='white', height=30)
        self.Delta_Jet_Current_Dig.grid(row=4, column=3, sticky='NEWS', pady=4, ipady=2, padx=4, ipadx=2)

        self.Delta_Status_Led = tk_tools.Led(self, size=50)
        self.Delta_Status_Led.grid(row=5, column=3, sticky='NSEW', ipadx=10)

        self.Starboard_Jet_Current_Label = Label(self, text="Starboard Jet Current:")
        self.Starboard_Jet_Current_Label.grid(row=3, column=4, sticky='NESW')

        self.Starboard_Jet_Current_Dig = tk_tools.SevenSegmentDigits(self, digits=10, background='black', digit_color='white', height=30)
        self.Starboard_Jet_Current_Dig.grid(row=4, column=4, sticky='NEWS', pady=4, ipady=2, padx=4, ipadx=2)


        #Rotary Scale
        self.rs = tk_tools.RotaryScale(self, max_value=360, size=100, unit='deg')
        self.rs.grid(row=0, column=8, rowspan=3)

        #Start Log Button
        self.StLog = Button(self, text="Start Log", command=print("Hello"))
        self.StLog.grid(row=2, column=0, sticky='N')

        


  

    def update_spdgauge(self):
        global speed_reading

        self.spdgauge.set_value(speed_reading)

    def update_pvgauge(self):
        global pack_voltage

        self.pvgauge.set_value(pack_voltage)
    
    def update_compass(self):
        global mag_compass_reading

        self.rs.set_value(round(mag_compass_reading, 2))

    def update_telemetry(self):
        global mag_compass_reading
        global target_heading
        global magnitude
        global mag_compass_reading
        global time_reading
        global lat_reading
        global lon_reading
        global speed_reading
        global gps_heading_reading
        global gps_distance

        self.Mag_Compass_Dig.set_value(str(round(mag_compass_reading, 2)))
        self.Latitude_Dig.set_value(str(round(lat_reading, 7)))
        self.Longitude_Dig.set_value(str(round(lon_reading, 7)))
        #self.GPS_Time_Dig.set_value(str(time_reading))
        self.Target_Heading_Dig.set_value(str(round(target_heading, 2)))
        #self.Magnitude_Dig.set_value(str(round(lat_reading, 7)))
        self.GPS_Speed_Dig.set_value(str(round(speed_reading, 2)))
        self.GPS_Compass_Dig.set_value(str(round(gps_heading_reading, 2)))
        self.GPS_Distance_Dig.set_value(str(round(gps_distance, 5)))

        self.Port_Jet_Current_Dig.set_value(str(round(jet2_current, 2)))
        self.Starboard_Jet_Current_Dig.set_value(str(round(jet1_current, 2)))

        self.Delta_Status_Led.to_grey()

        delta= abs(jet1_current-jet2_current)
        if delta > 10:
            self.Delta_Status_Led.to_red(on=FALSE)


        self.Delta_Jet_Current_Dig.set_value(str(round(delta, 2)))

        # self.Log_Led = tk_tools.Led(self, size=50)
        # self.Log_Led.grid(row=2, column=1, sticky='NSEW', ipadx=10)

        # def start_log(self):
        #     self.Log_Led.to_red(on=TRUE)

        # #Start Log Button
        # self.StLog = Button(self, text="Start Log", command=start_log)
        # self.StLog.grid(row=2, column=0, sticky='N')

        
        
        # Mag_Compass_Data = Label(self, text=round(mag_compass_reading,2))
        # Mag_Compass_Data.grid(row=3, column=1, sticky='W')

        # Target_Heading_Data = Label(self, text=round(target_heading,2))
        # Target_Heading_Data.grid(row=4, column=1, sticky='W')

        # GPS_Compass_Data = Label(self, text=round(gps_heading_reading,2))
        # GPS_Compass_Data.grid(row=5, column=1, sticky='W')

        # GPS_Time_Data = Label(self, text=round(time_reading,2))
        # GPS_Time_Data.grid(row=6, column=1, sticky='W')

        # Latitude_Data = Label(self, text=round(lat_reading,2))
        # Latitude_Data.grid(row=7, column=1, sticky='W')

        # Longitude_Data = Label(self, text=round(lon_reading,2))
        # Longitude_Data.grid(row=8, column=1, sticky='W')

        # GPS_Speed_Data = Label(self, text=round(speed_reading,2))
        # GPS_Speed_Data.grid(row=9, column=1, sticky='W')

        # GPS_Distance_Data = Label(self, text=round(gps_distance,2))
        # GPS_Distance_Data.grid(row=10, column=1, sticky='W')

        
    def updater(self):
        self.update_spdgauge()
        self.update_pvgauge()
        self.update_compass()
        self.update_telemetry()
        self.after(100, self.updater)

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

def on_vector_received(client, userdata, message):
    global target_heading
    global magnitude

    obj = json.loads(message.payload.decode('utf-8'))
    target_heading = obj["heading"]
    magnitude = obj["magnitude"]

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
            "/status/temp" : on_temp_received,
            "/status/vector" : on_vector_received
            #"/command/logging" : on_log_received
        }
        subber = Subscriber(client_id="teleGUI_live", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        while True:
            root = tk.Tk()
            root.title("RWM")
            app = Application(root)
            root.mainloop()
            
            
            
            
        
    except KeyboardInterrupt:
        exit
