from rpi_hardware_pwm import HardwarePWM
import time
import sys
import evdev
import os
import re
import numpy as np

pwm_motor = HardwarePWM(pwm_channel=2, hz=16_000, chip=2) #GPIO 18
pwm_motor.start(0) # zero duty cycle
pwm_servo = HardwarePWM(pwm_channel=3, hz=50, chip=2) #GPIO 19
pwm_servo.start(0)
os.system("pinctrl set 17 op dl")
relayvalue = False
eventfile = ""

def file_w_event(fpath):
    global eventfile
    #return os.path.isfile(fpath) and os.path.getsize(fpath) > 0
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

for event in evdev.InputDevice(eventfile).read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        if event.code == evdev.ecodes.BTN_SOUTH and event.value == 1:
            if relayvalue == True:
                os.system("pinctrl set 17 op dl")
                relayvalue = False
            else:
                os.system("pinctrl set 17 op dh")
                relayvalue = True

    if event.type == evdev.ecodes.EV_ABS:
        #Drive forwards
        if event.code == evdev.ecodes.ABS_GAS:
            val_speed = 65 / 1023 * event.value + 35
            os.system("pinctrl set 4 op dl")
            pwm_motor.change_duty_cycle(val_speed)
            print(val_speed)
        #Drive backwards
        if event.code == evdev.ecodes.ABS_BRAKE:
            val_speed = 65 / 1023 * event.value + 35
            os.system("pinctrl set 4 op dh")
            pwm_motor.change_duty_cycle(val_speed)
            print(-val_speed)
        #Steer left and right
        if event.code == evdev.ecodes.ABS_X:
            angle = 3
            if event.value < 28000:
                angle = np.interp(event.value, [0, 28000], [2, 3])
                print("Left")
            elif event.value > 36000:
                angle = np.interp(event.value, [36000, 65535], [3, 4])
                print("Right")
            else:
                angle = 3
                print("Neutral")
            pwm_servo.change_duty_cycle(angle)
