from rpi_hardware_pwm import HardwarePWM
import time
import sys
import evdev
import os

pwm = HardwarePWM(pwm_channel=0, hz=16_000, chip=2)
pwm.start(0)
os.system("pinctrl set 17 op dl")
relayvalue = False

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

        if event.code == evdev.ecodes.ABS_GAS:
            os.system("pinctrl set 4 op dl")
            print(val)
            pwm.change_duty_cycle(val)
        if event.code == evdev.ecodes.ABS_BRAKE:
            os.system("pinctrl set 4 op dh")
            print(-val)
            pwm.change_duty_cycle(val)
