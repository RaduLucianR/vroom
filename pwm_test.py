import numpy as np
import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
servo = GPIO.PWM(12,10000)
servo.start(0)

def map_value(value, in_min, in_max, out_min, out_max):
  return np.interp(value, [in_min, in_max], [out_min, out_max])


#angle = round(map_value(event.value, 0, 65535, 2, 12))
#print(angle)
#
for i in range(10, 100, 10):
    print(i)
    servo.ChangeDutyCycle(i)
    time.sleep(3)
servo.ChangeDutyCycle(70)

#servo.stop()
