from rpi_hardware_pwm import HardwarePWM
import time
import sys
import evdev
import os

pwm = HardwarePWM(pwm_channel=0, hz=50, chip=2)
pwm.start(0) # full duty cycle

for event in evdev.InputDevice("/dev/input/event13").read_loop():
    if event.type == evdev.ecodes.EV_ABS:
        val = 65 / 1023 * event.value + 35

        if event.code == evdev.ecodes.ABS_GAS:
            os.system("pinctrl set 4 op dh")
            print(val)
            pwm.change_duty_cycle(val)
        if event.code == evdev.ecodes.ABS_BRAKE:
            os.system("pinctrl set 4 op dl")
            print(-val)
            pwm.change_duty_cycle(val)
