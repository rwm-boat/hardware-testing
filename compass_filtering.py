import matplotlib.pyplot as plt
import json
import numpy as np
import os
import math
from scipy.signal import butter, lfilter, freqz
from scipy import signal
# import filterpy.kalman as kf
from filterpy.kalman import KalmanFilter
from filterpy.stats import gaussian
import easygui

gps_speed = []
gps_course = []
mag_compass = []
vector = []
kalman_live = []
live_lp = []
previous = 0

#PATH = "/home/actual_daniel/Documents/Logs/11-8-19/Waypoint1Sec_2019-11-8-21:20:50.txt"
PATH = easygui.fileopenbox()


# load log data into arrays
def load_log():

    global gps_speed
    global gps_course
    global mag_compass

    with open(PATH, "r") as log_file:
        for line in log_file.readlines():
            obj = json.loads(line)
            
            mag_compass.append(float(obj['mag_compass']))
            # gps_course.append(float(obj['gps_heading']))
            # gps_speed.append(float(obj['speed']))
            # vector.append(float(obj['vector']))
            # kalman_live.append(float(obj['kalman']))
            # live_lp.append(float(obj['compass_lp']))



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

def pva_kalman_filter():

    ## Measurement Noise Matrix
    R_std = 1
    ## Variance in white noise
    Q = 0.01 
    ## Discrete Time Step
    dt = 0.1

    kf = KalmanFilter(dim_x=3,dim_z=1)

    ### x = [x, xdx, xdx^2] (position, velocity, acceleration)
    kf.x = np.zeros(3)
    print(kf.x)

    ### Covariance Matrix
    ## Setting the initial convariance's for position, velocity and acceleration
    kf.P[0, 0] = 360
    kf.P[1, 1] = 1 ## No Clue - Change Later
    kf.P[2, 2] = 1 ## No Clue - Change Later
 
    kf.R *= R_std**2

    kf.Q = kf.Q_discrete_white_noise(3, dt, Q)


    ### Measurement Function
    kf.F = np.array([[1., dt, .5*dt*dt],
                    [0., 1.,       dt],
                    [0., 0.,       1.]])

    kf.H = np.array([[1., 0., 0.]])




# def kalman_filter(data):
    
#     output = []

#     ### sqrt of the variance is the error distance (aka. meters or degrees) ###
#     # how much error there is in the process model (how much do we trust the model)
#     process_var = .1
#     # how much error there is in each sensor measurement (how much do we trust the sensor)
#     sensor_var = 5

#     ## Initial State ##
#     # [position, variance, sensor_var] sensor state
#     # [(meters, degrees), (meters, degrees), ] ## remember sqrt of variance is distance error
#     x = gaussian(data[1], 20**2., sensor_var) 

#     #[position, velocity, process_var] of model initial state
#     # how we think the system works
#     process_model = gaussian(0., 0., process_var)

#     for z in data:
#         # -------- PREDICT --------- #
#         # X is the state of the system
#         # P is the variance of the system
#         # u is the movement of the system due to the process
#         # Q is the noise of the process
#         x, P = kf.predict(x=x, P=process_model)
#         # sensor says z with a standard deviation of sensorvar**2
#         # probability of the measurement given the current state 
#         #likelihood = gaussian(z, mean(z), sensor_var) 

#         # -------- UPDATE --------- #
#         # X is the state of the system
#         # P is the variance of the system
#         # z is the measurement
#         # R is the measurement variance
#         x, P = kf.update(x=x, P=P, z=z, R=sensor_var)
#         #print( "x: ",'%.3f' % x, "var: " '%.3f' % P, "z: ", '%.3f' % z)
#         #print(x)
#         output.append(x.mean())
#     return output

def low_pass_simple(data):
    global previous
    a = .2
    out = []
    for d in data:
        output = (a*d) + (1-a) * previous
        out.append(output)
        previous = output
    return out

#Plot of compass heading and speed
def generate_plot():


    kalman_filter = pva_kalman_filter()
    mu, cov, _, _ = kalman_filter.batch_filter(mag_compass)


    fig, ax1 = plt.subplots()

    ax1.plot(mag_compass, label="Magnometer Heading", color = 'g')
    ax1.plot(mu[:, 0], mu[:, 2], label="dual kalman", color = 'r')
    
    #ax1.plot(moving_avg_filter(mag_compass, 10), label="Moving Average Mag Compass: " + str(10), color = 'c')
    #ax1.plot(live_lp, label="live low pass", color = 'r')
    ax1.plot(kalman_live, label="kalman live", color = 'k')
    ax1.plot(low_pass_simple(kalman_live), label="kalman live + brent lp", color = 'r')
    #ax1.plot(low_pass_filter(kalman_live,.2,10), label="kalman live + low pass filter", color = 'b')


    ax1.legend(loc = 'lower right')
   
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    plt.title("Boat Speed and Course " + os.path.basename(PATH))
    ax1.set_xlabel("Time (1/10 sec)")
    ax1.set_ylabel('Heading (degrees)')
    ax2.set_ylabel("GPS Speed (kn)")
    
    ax1.grid()
    plt.show()

pva_kalman_filter()
load_log()
generate_plot()