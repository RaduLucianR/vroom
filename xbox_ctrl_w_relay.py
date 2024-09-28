from rpi_hardware_pwm import HardwarePWM
import time
import sys
import evdev
import os
import numpy as np

# pwm channel = 0 and chip = 0 for rpi4 for gpio 18
# pwm channel = 2 and chip = 2 for rpi5 for gpio 18
pwm = HardwarePWM(pwm_channel=3, hz=50, chip=2) # 50Hz for servo
# 16 kHz for motor
pwm.start(0)
os.system("pinctrl set 17 op dl")
relayvalue = False
#pwm.change_duty_cycle(100)

try:
    for event in evdev.InputDevice("/dev/input/event13").read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.code == evdev.ecodes.BTN_SOUTH and event.value == 1:
                if relayvalue == True:
                    os.system("pinctrl set 17 op dl")
                    relayvalue = False
                else:
                    os.system("pinctrl set 17 op dh")
                    relayvalue = True
        
        if event.type == evdev.ecodes.EV_ABS:
            val = 65 / 1023 * event.value + 35
            angle = round(np.interp(event.value, [0, 1023], [2, 4]))
            if event.code == evdev.ecodes.ABS_GAS:
                os.system("pinctrl set 4 op dl")
                #print(val)
                print(angle)
                #pwm.change_duty_cycle(val) # for BLDC
                pwm.change_duty_cycle(angle) # for servo
            if event.code == evdev.ecodes.ABS_BRAKE:
                os.system("pinctrl set 4 op dh")
                print(-val)
                pwm.change_duty_cycle(val)
            if event.code == evdev.ecodes.ABS_X:
                #angle = round(np.interp(event.value, [0, 65535], [2, 4]))
                if event.value < 28000:
                    angle = 2
                elif event.value > 36000:
                    angle = 4
                else:
                    angle = 3
                print(event.value)
                pwm.change_duty_cycle(angle)
except:
    print("closing pwm")
    pwm.stop()
