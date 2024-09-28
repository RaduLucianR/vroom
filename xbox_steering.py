import pigpio
import time

# GPIO pin connected to the servo signal line
SERVO_PIN = 17  # Change this to your actual GPIO pin number

# Servo pulse width range (in microseconds)
MIN_PULSE_WIDTH = 500    # Minimum pulse width (corresponds to 0 degrees)
MAX_PULSE_WIDTH = 2500   # Maximum pulse width (corresponds to 180 degrees)

# Initialize pigpio library
pi = pigpio.pi()

if not pi.connected:
    exit()

def set_servo_angle(angle):
    if 0 <= angle <= 180:
        pulse_width = MIN_PULSE_WIDTH + (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) * (angle / 180)
        pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
    else:
        print("Angle must be between 0 and 180 degrees")

try:
    while True:
        # Sweep the servo from 0 to 180 degrees and back
        for angle in range(0, 181, 10):
            set_servo_angle(angle)
            time.sleep(0.5)
        for angle in range(180, -1, -10):
            set_servo_angle(angle)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("Program terminated")

finally:
    # Stop PWM and cleanup
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    pi.stop()
