import matplotlib.pyplot as plt
import json
import numpy as np
import os
import math

gps_speed = []
gps_course = []
mag_compass_reading = []

mag_compass_mv_val = 0
mag_compass_mvavg = []
mag_compass_mvavg_n = 30
mag_compass_avg = []

PATH = "C:/Users/Daniel-LT/Documents/WPI/MQP/Logs"


def load_log():


    global gps_speed
    global gps_course
    global mag_compass_reading
    global mag_compass_mv_val
    global mag_compass_mvavg

    with open(PATH, "r") as log_file:
        error_filter = 20
        for line in log_file.readlines():
            obj = json.loads(line)
            
            #Populate Mag Compass Array
            mag_compass_reading.append(obj['mag_compass'])
            #Populate GPS Arrays
            gps_course.append(obj['course'])
            gps_speed.append(obj['speed'])
            #Calculate Mag Compass Moving Average then populate array
            if len(mag_compass_mvavg) < mag_compass_mvavg_n:
                mag_compass_mvavg.append(float((obj['mag_compass'])))
            else:
                del mag_compass_mvavg[0]
                mag_compass_mvavg.append(float((obj['mag_compass'])))
            mag_compass_mv_val = sum(mag_compass_mvavg)/mag_compass_mvavg_n
            mag_compass_avg.append(mag_compass_mv_val)


#Plot of compass heading and speed
def generate_plot():
    fig, ax1 = plt.subplots()

    ax1.plot(mag_compass_reading, label="Magnometer Heading", color = 'g')
    ax1.plot(gps_course, label="GPS Heading", color = 'R')
    ax1.plot(mag_compass_avg, label="Moving Average Mag Compass: " + str(mag_compass_mvavg_n), color = 'k')
    ax1.legend(loc = 'lower right')
   
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    ax2.plot(gps_speed, label="GPS Speed")
    ax2.legend(loc = 'upper right')

    # ax3.plot(jet1_current, label="Jet 1 Amps", color = 'g', linestyle = '--')
    # ax3.plot(jet2_current, label="Jet 2 Amps", color = 'r', linestyle = "--")
    # ax3.legend(loc = 'center bottom')

    plt.title("Boat Speed and Course " + os.path.basename(PATH))
    ax1.set_xlabel("Time (1/10 sec)")
    ax1.set_ylabel('Heading (degrees)')
    ax2.set_ylabel("GPS Speed (kn)")
    
    ax1.grid()
    plt.show()


load_log()
#plot_adc_speed_log(jet1_current,jet2_current, speed)
generate_plot()
print("here")
#plot_adc_temp_log(jet1_current,jet2_current,jet1_temp,jet2_temp, compartment_temp)