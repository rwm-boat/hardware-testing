from tkinter import *
import tkinter as tk
import tk_tools

import sys,os
import time
#from mqtt_client.subscriber import Subscriber
from threading import Thread
import json

root = tk.Tk()
root.title("CPU Temp")

pack_voltage_gauge = tk_tools.Gauge(root, height = 200, width = 400,
                             min_value=10,
                             max_value=40,
                             label='Pack Voltage',
                             unit=' V',
                             divisions=30,
                             yellow=66,
                             red=70,
                             yellow_low=43,
                             red_low=40)
                             #bg='grey')
pack_voltage_gauge.grid(row=0, column=1, rowspan=3, sticky='news')

def update_gauge():
    # Get the Raspberry CPU Temp
    tFile = open('/sys/class/thermal/thermal_zone0/temp')
    # Scale the temp from milliC to C
    thetemp = int(float(tFile.read())/1000)
    pack_voltage_gauge.set_value(thetemp)

    # update the gauges according to their value

    root.after(1000, update_gauge)

FiNaEn = Entry(root)
FiNaEn.grid(row=1, column=0)
FiNaLa = Label(root, text="File name:")
FiNaLa.grid(row=0, column=0, sticky='S')

StLog = Button(root, text="Start Log")
StLog.grid(row=2,column=0, sticky='N')


if __name__ == '__main__':

    try:
        root.mainloop()
        while True:
            root.after(1000, update_gauge)
            
            
        
    except KeyboardInterrupt:
        exit