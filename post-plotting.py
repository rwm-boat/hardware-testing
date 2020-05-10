import matplotlib.pyplot as plt
import json
import math
import easygui
import numpy as np
import os

path = easygui.fileopenbox()

jet1_current = []
jet2_current = []
time = []
latitude = []
longitude = []
speed_reading = []
course = []
mag_compass_reading = []
int_compass_reading = []
jet1_motor_temp = []
jet2_motor_temp = []
jet1_esc_temp = []
jet2_esc_temp =[]
MPA_temp = []
gps_distance = []

mag_compass_mv_val = 0
mag_compass_mvavg = []
mag_compass_mvavg_n = 30
mag_compass_avg = []

def load_log():

    global jet1_current
    global jet2_current
    global time
    global latitude
    global longitude
    global speed_reading
    global course
    global mag_compass_reading
    global int_compass_reading
    global jet1_motor_temp
    global jet2_motor_temp
    global jet1_esc_temp
    global jet2_esc_temp
    global MPA_temp
    global gps_distance
    global mag_compass_mv_val
    global mag_compass_mvavg

    with open(path, "r") as log_file:
        error_filter = 20
        for line in log_file.readlines():
            obj = json.loads(line)
            #current
            jet1_current.append((obj["jet1_current"]))
            jet2_current.append((obj["jet2_current"]))
            #gps
            time.append(obj["time_reading"])
            if abs(int(obj["lat_reading"])) > error_filter:
                latitude.append(obj["lat_reading"])
            if abs(obj["lon_reading"]) > error_filter:
                longitude.append(obj["lon_reading"])
            speed_reading.append(obj["speed_reading"])
            course.append(obj["gps_heading_reading"])
            #temperature sensors
            jet1_motor_temp.append(obj["jet1_motor_temp"])
            jet2_motor_temp.append(obj["jet2_motor_temp"])
            jet1_esc_temp.append(obj["jet1_esc_temp"])
            jet2_esc_temp.append(obj["jet2_esc_temp"])
            MPA_temp.append(obj["MPA_temp"])
            #internal compass
            int_compass_reading = obj['int_compass_reading']
            #mag compass
            mag_compass_reading.append(obj['mag_compass_reading'])
            
            if len(mag_compass_mvavg) < mag_compass_mvavg_n:
                mag_compass_mvavg.append(float((obj['mag_compass_reading'])))
            else:
                del mag_compass_mvavg[0]
                mag_compass_mvavg.append(float((obj['mag_compass_reading'])))
            mag_compass_mv_val = sum(mag_compass_mvavg)/mag_compass_mvavg_n
            mag_compass_avg.append(mag_compass_mv_val)
            

#Create plot of current vs. boat speed
def plot_adc_speed_log(jet1_current, jet2_current, speed_reading):
    fig, ax1 = plt.subplots()

    ax1.plot(jet1_current, label="Jet 1 Amps", color = 'g')
    ax1.plot(jet2_current, label="Jet 2 Amps", color = 'r')
    
    ax2 = ax1.twinx() #second y axis
    ax2.plot(speed_reading, label="Speed (knots)", linewidth=3.3)
    ax2.legend(loc = 'upper right')
    
    plt.title("Jet Current Draw and Boat Speed")
    ax1.set_xlabel("Time (deciseconds)")
    ax1.set_ylabel("Jet Current Draw (Amps)")
    ax2.set_ylabel("Boat Speed (knots)")
    ax1.legend(loc = 'lower right')
    ax1.grid()
    maxSpeed = round(max(speed_reading), 2)
    maxJet1Cur = round(max(jet1_current), 2)
    maxJet2Cut = round(max(jet2_current), 2)

    textstr = '\n'.join((r"Max Speed = %s (Kn)" % (maxSpeed),
        r"Jet 1 Max Current = %s (Amps)" % (maxJet1Cur),
        r"Jet 2 Max Current = %s (Amps)" % (maxJet2Cut)))
    box = dict(boxstyle='round', facecolor='gray', alpha=0.5)
    ax1.text(0, maxJet1Cur, textstr, fontsize=12, verticalalignment='top', bbox=box)

    plt.show()
    
    


#Plot of temperature and current
def plot_adc_temp_log(jet1_current, jet2_current, jet1_motor_temp, jet2_motor_temp, jet1_esc_temp, jet2_esc_temp):
    fig, ax1 = plt.subplots()

    ax1.plot(jet1_current, label="Jet 1 Amps", color = 'g')
    ax1.plot(jet2_current, label="Jet 2 Amps", color = 'r')
    
    ax2 = ax1.twinx()
    ax2.plot(jet1_motor_temp, label="Jet 1 Motor Temp")
    ax2.plot(jet2_motor_temp, label="Jet 2 Motor Temp")
    ax2.plot(jet1_esc_temp, label="Jet 1 ESC Temp")
    ax2.plot(jet2_esc_temp, label="Jet 2 ESC Temp")
    # ax2.legend()

    plt.title("Jet Amperage vs. Temperature")
    ax1.set_xlabel("Time (1/10 sec)")
    ax1.set_ylabel('Amperes')
    # ax2.set_ylabel("Temperature Celcius")
    ax1.legend()
    ax1.grid()

    plt.show()

#Plot of compass heading and speed
def plot_mag_course(mag_compass_reading, course, speed, mag_compass_avg):
    fig, ax1 = plt.subplots()

    ax1.plot(mag_compass_reading, label="Magnometer Heading", color = 'g')
    ax1.plot(course, label="GPS Heading", color = 'R')
    ax1.plot(mag_compass_avg, label="Moving Average Mag Compass: " + str(mag_compass_mvavg_n), color = 'k')
    ax1.legend(loc = 'lower right')
   
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    ax2.plot(speed, label="GPS Speed")
    ax2.legend(loc = 'upper right')

    # ax3.plot(jet1_current, label="Jet 1 Amps", color = 'g', linestyle = '--')
    # ax3.plot(jet2_current, label="Jet 2 Amps", color = 'r', linestyle = "--")
    # ax3.legend(loc = 'center bottom')

    plt.title("Boat Speed and Course " + os.path.basename(path))
    ax1.set_xlabel("Time (1/10 sec)")
    ax1.set_ylabel('Heading (degrees)')
    ax2.set_ylabel("GPS Speed (kn)")
    
    ax1.grid()
    plt.show() 


load_log()
plot_adc_speed_log(jet1_current,jet2_current, speed_reading)
#plot_mag_course(mag_compass_reading, course, speed, mag_compass_avg)
#plot_adc_temp_log(jet1_current,jet2_current,jet1_motor_temp,jet2_motor_temp,jet1_esc_temp,jet2_esc_temp)


