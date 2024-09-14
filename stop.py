from rpi_hardware_pwm import HardwarePWM
import time

pwm = HardwarePWM(pwm_channel=0, hz=16_000, chip=2)
pwm.start(0) # full duty cycle

pwm.stop()
