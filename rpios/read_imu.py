import mpu6050
import time
import math
import numpy as np
from skinematics import imus
from collections import deque

def calc_bias(nrof_samples: int):
	print("Calibrating...")
	acc_bias = np.zeros(3)
	ang_vel_bias = np.zeros(3)
	acc_data = []
	ang_vel_data = []
	
	for i in range(nrof_samples):
		acc, ang_vel, temp = read_sensor_data()
		acc_data.append(list(acc.values()))
		ang_vel_data.append(list(ang_vel.values()))
		time.sleep(0.1)
	
	acc_data = np.array(acc_data)
	ang_vel_data = np.array(ang_vel_data)
	acc_bias = np.mean(acc_data, axis = 0) # Axis 0 means: for each column across all rows
	ang_vel_bias = np.mean(ang_vel_data, axis = 0)
	
	print("Finished calibrating!")
	print("Acceleration bias:", acc_bias, "   Angular velocity: ", ang_vel_bias)
	return acc_bias[2] - 9.81, ang_vel_bias

def apply_calibration(acc, ang_vel, acc_bias, ang_vel_bias):
	return acc - acc_bias, ang_vel - ang_vel_bias
		

def read_sensor_data():
	a = mpu6050.get_accel_data()
	gyro = mpu6050.get_gyro_data()
	temp = mpu6050.get_temp()	
	
	return a, gyro, temp

mpu6050 = mpu6050.mpu6050(0x68)
period = 0.5
sampling_rate = 1 / period

init_orientation = np.array([
							[1, 0, 0],
							[0, 1, 0],
							[0, 0, 1]
						   ])
init_position = np.array([0, 0, 0])
i = 0
window_size = 15
alpha = 0.1
acc_bias, ang_vel_bias = calc_bias(50)


# First measurement
data = read_sensor_data()
acc = np.array(list(data[0].values()))
ang_vel = np.array(list(data[1].values()))
ang_vel_matrix = ang_vel
acc_matrix = acc
acc_window = deque(maxlen = window_size)
ang_vel_window = deque(maxlen = window_size)
acc_window.append(acc)
ang_vel_window.append(ang_vel)

while True:
	data = read_sensor_data()
	acc = np.array(list(data[0].values()))
	ang_vel = np.array(list(data[1].values()))
	ang_vel_matrix = np.vstack([ang_vel_matrix, ang_vel])
	acc_matrix = np.vstack([acc_matrix, acc])
	acc = acc - acc_bias
	ang_vel = ang_vel - ang_vel_bias
	#print(acc, ang_vel)
		
	
	if i > 3:
		q, pos, vel = imus.analytical(init_orientation, ang_vel_matrix, init_position, acc_matrix, sampling_rate)
		print(q[-1])
	
	time.sleep(period)
	i += 1
