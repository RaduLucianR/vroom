from rpi_hardware_pwm import HardwarePWM
import time
import sys
import evdev
import os
import re

pwm_motor = HardwarePWM(pwm_channel=0, hz=16_000, chip=0) #GPIO 18
pwm_motor.start(0) # zero duty cycle
time.sleep(3)
pwm_motor.change_duty_cycle(50)
time.sleep(3)
pwm_motor.change_duty_cycle(100)
ime.sleep(3)
pwm_motor.change_duty_cycle(0)
