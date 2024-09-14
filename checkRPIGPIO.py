import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)
pin = 17  # Replace with your GPIO pin number
GPIO.setup(pin, GPIO.OUT)

# Blink LED
for _ in range(10):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()
