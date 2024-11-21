import lgpio
import time

MOTOR_PIN = 18
STEER_PIN = 19
TRANSISTOR_PIN = 17
h = lgpio.gpiochip_open(4)
FREQ_MOTOR = 10000
FREQ_STEER = 50

lgpio.gpio_claim_output(h, TRANSISTOR_PIN)
lgpio.gpio_write(h, TRANSISTOR_PIN, 1)

lgpio.gpio_claim_output(h, MOTOR_PIN)
lgpio.gpio_write(h, MOTOR_PIN, 0)

'''
try:
	time.sleep(3)
	lgpio.tx_pwm(h, MOTOR_PIN, FREQ_MOTOR, 100)
	lgpio.tx_pwm(h, STEER_PIN, FREQ_STEER, 100)
except KeyboardInterrupt:
	lgpio.tx_pwm(h, MOTOR_PIN, FREQ, 0)
	lgpio.gpiochip_close(h)
  '''
