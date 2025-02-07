import time
import evdev
import os
import numpy as np

# PINs
TRANSISTOR_PIN = 0 # i.e. GPIO 0, aka BCM 17, physical 11
GAS_PIN = 1 # i.e. GPIO 1, aka BCM 18, physical ??
STEER_PIN = 24 # i.e. GPIO 24, aka BCM 19, physical 35
BACKWARDS_PIN = 7 # i.e. GPIO 7, aka BCM 4, physical 7
HIGH = 1
LOW = 0

# Initialize PINs
os.system(f"gpio mode {TRANSISTOR_PIN} out") # set pin to mode "out"
os.system(f"gpio mode {BACKWARDS_PIN} out")
os.system(f"gpio mode {GAS_PIN} pwm")
#os.system("gpio pwmc 119")
os.system("gpio pwmr 100")
os.system(f"gpio mode {STEER_PIN} pwm")

relayvalue = False
eventfile = ""

def file_w_event(fpath):
    global eventfile

    with open('xboxevent.txt', 'r') as file:
        first_line = file.readline().strip()
        
        if first_line.startswith("event"):
            eventfile = f"/dev/input/{first_line}"
            return True
        else:
            return False
    
while not file_w_event("./xboxevent.txt"):
    print("No Xbox Controller detected!")
    time.sleep(3)
    
print("Controller detected!!!")

try:
	for event in evdev.InputDevice(eventfile).read_loop():
		if event.type == evdev.ecodes.EV_KEY:
			if event.code == evdev.ecodes.BTN_SOUTH and event.value == 1:
				if relayvalue == True:
					os.system(f"gpio write {TRANSISTOR_PIN} {LOW}")
					relayvalue = False
				else:
					os.system(f"gpio write {TRANSISTOR_PIN} {HIGH}")
					relayvalue = True
		if event.type == evdev.ecodes.EV_ABS:
			#Drive forwards
			if event.code == evdev.ecodes.ABS_Z:
				val_speed = 65 / 1023 * event.value + 35
				os.system(f"gpio write {BACKWARDS_PIN} {LOW}")
				os.system("gpio pwmr 100")
				os.system(f"gpio pwm {GAS_PIN} {val_speed}")
				print("forwards:", val_speed)
			#Drive backwards
			if event.code == evdev.ecodes.ABS_RZ:
				val_speed = 65 / 1023 * event.value + 35
				os.system(f"gpio write {BACKWARDS_PIN} {HIGH}")
				#os.system("gpio pwmc 119")
				os.system("gpio pwmr 100")
				os.system(f"gpio pwm {GAS_PIN} {val_speed}")
				print("backwards:", val_speed)
			if event.code == evdev.ecodes.ABS_X:
				angle = 350
				if event.value < -1000:
					angle = np.interp(event.value, [-32768, -1000], [200, 350])
					print("Left")
				elif event.value > 1000:
					angle = np.interp(event.value, [1000, 32768], [350, 500])
					print("Right")
				else:
					angle = 350
					print("Neutral")
				os.system(f"gpio pwmr 1024")
				os.system(f"gpio pwm {STEER_PIN} {angle}")
except KeyboardInterrupt:
	print("\nExit gracefully!")
	os.system(f"gpio write {TRANSISTOR_PIN} {LOW}") # Cut gas and steering from power
except Exception as e:
	print("\nShut down gas and steering because exception!")
	os.system(f"gpio write {TRANSISTOR_PIN} {LOW}")
	raise e
