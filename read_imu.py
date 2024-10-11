import mpu6050
import time

mpu6050 = mpu6050.mpu6050(0x68)

def read_sensor_data():
	a = mpu6050.get_accel_data()
	gyro = mpu6050.get_gyro_data()
	temp = mpu6050.get_temp()
	
	return a, gyro, temp
	
while True:
	data = read_sensor_data()
	print(f"Acceleration: {data[0]}, Gyro: {data[1]}, Temperature: {data[2]}")
	time.sleep(0.2)
