import time
import os

while True:
	
	val = os.system("pinctrl get 21")
	print(val)
	time.sleep(0.001)
