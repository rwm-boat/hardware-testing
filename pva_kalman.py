from filterpy.kalman import KalmanFilter
from filterpy.stats import gaussian
from filterpy.common import Q_discrete_white_noise
import numpy as np
from numpy.random import randn
import matplotlib.pyplot as plt
import easygui
import json

# PATH = "/Users/Daniel-LT/Documents/WPI/MQP/Logs/circle_2_2019-11-10-20_19_37.txt"
PATH = easygui.fileopenbox()

mag_compass = []
kalman_live = []
pys = []

def load_log():

	with open(PATH, "r") as log_file:
		for line in log_file.readlines():
			obj = json.loads(line)
			
			mag_compass.append(float(obj['mag_compass']))
			kalman_live.append(float(obj['kalman']))

def pva_kalman_filter():
	
	kf = KalmanFilter(dim_x=3, dim_z=1)

	# Time Step
	dt = 0.1

	# Control Inputs
	kf.u = 0

	# Measurement Function (we are only recording position)
	kf.H = np.array([[1,0,0]])

	# State Variable
	kf.x = np.array([[0,0,0]]).T

	# Measurement Noise 
	kf.R = 20

	# Process/Motion Noise
	kf.Q = np.eye(3) * .1

	# Covariance Matrix
	kf.P = np.eye(3)*1

	# State Transition Function
	kf.F = np.array([[1., dt, .5*dt*dt],
						[0., 1.,       dt],
						[0., 0.,       1.]])
	## --------------- PREDICT / UPDATE -----------## 
	for z in mag_compass:
		kf.predict()
		kf.update(z)
		pys.append(kf.x[0])

## ---------------- PLOT -------------------------##
load_log()
pva_kalman_filter()
plt.plot(mag_compass, label = 'live compass')
plt.plot(pys, label = 'PVA Kalman', color='g')
plt.plot(kalman_live, label = 'P Kalman', color = 'k')
plt.legend(loc = 'lower right')
plt.grid()
plt.show()