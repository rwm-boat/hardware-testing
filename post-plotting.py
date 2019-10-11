import matplotlib.pyplot as plt
import json
import math
import easygui

path = easygui.fileopenbox()

jet1_current = []
jet2_current = []
time = []
latitude = []
longitude = []
speed = []
course = []
mag_compass_reading = []
int_compass_reading = []
jet1_temp = []
jet2_temp = []
compartment_temp = []
gps_distance = []

def load_log():

    global jet1_current
    global jet2_current
    global time
    global latitude
    global longitude
    global speed
    global course
    global mag_compass_reading
    global int_compass_reading
    global jet1_temp
    global jet2_temp
    global compartment_temp
    global gps_distance

    with open(path, "r") as log_file:
        error_filter = 20
        for line in log_file.readlines():
            obj = json.loads(line)
            #current
            jet1_current.append((obj["jet1_current"]-2.57)/0.013)
            jet2_current.append((obj["jet2_current"]-2.47)/0.013)
            #gps
            time.append(obj["time"])
            if abs(int(obj["latitude"])) > error_filter:
                latitude.append(obj["latitude"])
            if abs(obj["longitude"]) > error_filter:
                longitude.append(obj["longitude"])
            speed.append(obj["speed"])
            course.append(obj["gps_heading"])
            #temperature sensors
            jet1_temp.append(obj["jet1_temp"])
            jet2_temp.append(obj["jet2_temp"])
            compartment_temp.append(obj["compartment_temp"])
            #internal compass
            int_compass_reading = obj['int_compass']
            #mag compass
            mag_compass_reading = obj['mag_compass']


#Create plot of current vs. boat speed
def plot_adc_speed_log(jet1_current, jet2_current, speed):
    fig, ax1 = plt.subplots()

    ax1.plot(jet1_current, label="Jet 1 Amps", color = 'g')
    ax1.plot(jet2_current, label="Jet 2 Amps", color = 'r')
    
    ax2 = ax1.twinx()
    ax2.plot(speed, label="Speed (kn)")
    
    plt.title("Jet Amperage vs. Time")
    ax1.set_xlabel("Time (1/10 sec)")
    ax1.set_ylabel('Amperes')
    ax2.set_ylabel("Speed(kn)")
    ax1.legend()
    ax1.grid()
    plt.show()

#Plot of temperature and current
def plot_adc_temp_log(jet1_current, jet2_current, jet1_temp, jet2_temp, compartment_temp):
    fig, ax1 = plt.subplots()

    ax1.plot(jet1_current, label="Jet 1 Amps", color = 'g')
    ax1.plot(jet2_current, label="Jet 2 Amps", color = 'r')
    
    ax2 = ax1.twinx()
    ax2.plot(jet1_temp, label="Jet 1 Temp")
    ax2.plot(jet2_temp, label="Jet 2 Temp")
    ax2.plot(compartment_temp, label="Compartment Temp")
    ax2.legend()

    plt.title("Jet Amperage vs. Temperature")
    ax1.set_xlabel("Time (1/10 sec)")
    ax1.set_ylabel('Amperes')
    ax2.set_ylabel("Temperature Celcius")
    ax1.legend()
    ax1.grid()
    plt.show()


load_log()
plot_adc_speed_log(jet1_current,jet2_current, speed)
plot_adc_temp_log(jet1_current,jet2_current,jet1_temp,jet2_temp, compartment_temp)


