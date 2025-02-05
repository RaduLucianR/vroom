#!/usr/bin/python3

import sys
import site
site.addsitedir("/home/vroom/.local/lib/python3.12/site-packages")

from rpi_hardware_pwm import HardwarePWM
import time
import sys
import evdev
import os
import re

pwm_motor = HardwarePWM(pwm_channel=0, hz=16_000, chip=0) #GPIO 18
pwm_motor.start(0) # zero duty cycle
print("Init pwm")
time.sleep(3)
pwm_motor.change_duty_cycle(50)
print("50%")
time.sleep(3)
pwm_motor.change_duty_cycle(70)
print("70%")
time.sleep(3)
pwm_motor.change_duty_cycle(0)
print("0%")
