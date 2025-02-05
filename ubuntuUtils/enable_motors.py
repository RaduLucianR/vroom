import os

TRANSISTOR_PIN = 0 # i.e. GPIO 0, aka BCM 17, physical 11
os.system(f"gpio mode {TRANSISTOR_PIN} out")
os.system(f"gpio write {TRANSISTOR_PIN} 1") # set the pin high
