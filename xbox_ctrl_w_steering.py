from rpi_hardware_pwm import HardwarePWM
import time
import sys
import evdev
import os

pwm_motor = HardwarePWM(pwm_channel=0, hz=16_000, chip=2)
pwm_motor.start(0) # zero duty cycle
pwm_servo = HardwarePWM(pwm_channel=1, hz=6_667, chip=1)
pwm_servo.start(50)

for event in evdev.InputDevice("/dev/input/event13").read_loop():
    #Filter out only events we care about (throttle & steering)
    if event.type == evdev.ecodes.EV_ABS:
        #Drive forwards
        if event.code == evdev.ecodes.ABS_GAS:
            val_speed = 65 / 1023 * event.value + 35
            os.system("pinctrl set 4 op dh")
            pwm_motor.change_duty_cycle(val_speed)
            print(val_speed)
        #Drive backwards
        if event.code == evdev.ecodes.ABS_BRAKE:
            val_speed = 65 / 1023 * event.value + 35
            os.system("pinctrl set 4 op dl")
            pwm_motor.change_duty_cycle(val_speed)
            print(-val_speed)
        #Steer left and right
        if event.code == evdev.ecodes.ABS_X:
            period_req = (2000 / 65535 *event.value + 500)/1e6
            val_steering = 1/period_req # 65 / 1023 * event.value + 35
            pwm_servo.change_frequency(val_steering)
            print(val_steering)
        
