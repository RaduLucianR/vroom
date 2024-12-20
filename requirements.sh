#!/bin/bash

pip install mpu6050-raspberry
sudo apt install python3-smbus
pip install mpu6050 --break-system-package
pip install evdev --break-system-package
pip install rpi_hardware_pwm --break-system-package
sudo apt install evtest
