import matplotlib.pyplot as plt
import json
import numpy as np
import os
import math
from scipy.signal import butter, lfilter, freqz
from scipy import signal

gps_speed = []
gps_course = []
mag_compass = []

PATH = "/home/actual_daniel/125deg305_2019-11-7-15_35_22.txt"

# load log data into arrays
def load_log():

    global gps_speed
    global gps_course
    global mag_compass

    with open(PATH, "r") as log_file:
        error_filter = 20
        for line in log_file.readlines():
            obj = json.loads(line)
            
            mag_compass.append(float(obj['mag_compass']))
            gps_course.append(float(obj['gps_heading']))
            gps_speed.append(float(obj['speed']))

#enter the input array and number of terms, returns an array of the moving average
def moving_avg_filter(data, terms):
    mag_compass_mvavg = []
    result = []
    for x in data:
        if len(mag_compass_mvavg) < terms: mag_compass_mvavg.append(x)
        else:
            del mag_compass_mvavg[0]
            mag_compass_mvavg.append(x)
            result.append(sum(mag_compass_mvavg)/terms)
    return result

def low_pass_filter(data, cutoff_freq, sample_freq, order=5):

    w = cutoff_freq / (sample_freq / 2) # normalize frequency
    
    b, a = butter(order, w, 'low')
    output = signal.filtfilt(b, a, data)
    return output

#Plot of compass heading and speed
def generate_plot():

    fig, ax1 = plt.subplots()

    ax1.plot(mag_compass, label="Magnometer Heading", color = 'g')
    ax1.plot(gps_course, label="GPS Heading", color = 'R')
    
    ax1.plot(moving_avg_filter(mag_compass, 10), label="Moving Average Mag Compass: " + str(10), color = 'k')
    ax1.plot(low_pass_filter(mag_compass, .5, 10), label="lowpassfilter", color = 'c')
        
    ax1.legend(loc = 'lower right')
   
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    # ax2.plot(gps_speed, label="GPS Speed", linestyle='--')
    # ax2.legend(loc = 'upper right')

    plt.title("Boat Speed and Course " + os.path.basename(PATH))
    ax1.set_xlabel("Time (1/10 sec)")
    ax1.set_ylabel('Heading (degrees)')
    ax2.set_ylabel("GPS Speed (kn)")
    
    ax1.grid()
    plt.show()

load_log()
generate_plot()

