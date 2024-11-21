import gpiod
import time

chip = gpiod.Chip('gpiochip5')
line = chip.get_line(18)
duty_cycle = 0.7
frequency = 16_000

period = 1 / frequency
high_time = duty_cycle * period
low_time = (1 - duty_cycle) * period

config = gpiod.line_request()
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
line.request(config)

try:
    while True:
        line.set_value(1)
        time.sleep(high_time)
        line.set_value(0)
        time.sleep(low_time)
except KeyboardInterrupt:
    pass
finally:
    line.set_value(0)
    line.release()
