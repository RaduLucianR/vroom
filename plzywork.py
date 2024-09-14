from rpi_hardware_pwm import HardwarePWM
import time

pwm = HardwarePWM(pwm_channel=0, hz=16_000, chip=2)
pwm.start(0) # full duty cycle

#pwm.change_duty_cycle(50)

for i in range(10, 100, 10):
    pwm.change_duty_cycle(i)
    time.sleep(3)

pwm.stop()
