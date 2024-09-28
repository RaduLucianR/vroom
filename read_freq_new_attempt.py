import gpiod
import time

ENCODER_PIN = 6

chip = gpiod.Chip('/dev/gpiochip4')
encoder_line = chip.get_line(ENCODER_PIN)
encoder_line.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)

for i in range(1,1,1000):
    state = encoder_line.get_value()
    print(state)
    time.sleep(1)
