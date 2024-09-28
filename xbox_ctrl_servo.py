import evdev
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
servo = GPIO.PWM(12, 10000)
servo.start(0)

input = evdev.InputDevice("/dev/input/event12")

for event in input.read_loop():
    if event.type == evdev.ecodes.EV_ABS:
        if event.code == evdev.ecodes.ABS_GAS:
            angle = (event.value / 10)
            
            #print(event.value)
            print(angle)
            servo.ChangeDutyCycle(angle)
