from tkinter import *
import tkinter as tk
import tk_tools
from mqtt_client.publisher import Publisher

pubber = Publisher(client_id="log_command", broker_ip="192.168.1.170")
stop = False
class Application(tk.Frame):
    #GUI

    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        # self.updater()

    def create_widgets(self):
        global stop

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

        self.Log_Status_Led = tk_tools.Led(self, size=50)
        self.Log_Status_Led.grid(row=2, column=1, sticky='NSEW', ipadx=10)
        #Rotary Scale
        self.rs = tk_tools.RotaryScale(self, max_value=360, size=100, unit='deg')
        self.rs.grid(row=0, column=8, rowspan=3)

        #Start Log Button
        self.StLog = Button(self, text="Start Log", command=self.start_log)
        self.StLog.grid(row=2, column=0, sticky='N')

        self.Stop_Log = Checkbutton(self, text="Stop Logging", command=self.stop_log)
        self.Stop_Log.grid(row=0, column=1, sticky='N')

    def stop_log(self):
        global stop
        stop = not stop
        
        pubber.publish("/command/stop_logging", stop)
        

    def start_log(self):
        log_title = self.FiNaEn.get()
        pubber.publish("/command/logging", str(log_title))