import time
import os

# Configuration
UPDATE_INTERVAL = 0.001  # 1 ms update interval

def parse_gpio_status(status_text):
    if not isinstance(status_text, str):
        raise TypeError("Input must be a string")
    
    if "hi" in status_text:
        return 1
    elif "lo" in status_text:
        return 0
    else:
        raise ValueError("Invalid status text")

def calculate_frequency(values):
    last_value = None
    last_time = None
    edge_count = 0

    for current_time, value in values:
        if last_value is not None and value != last_value:
            # An edge has occurred
            edge_count += 1
            if last_time is not None:
                # Calculate time between edges
                time_between_edges = current_time - last_time
                # Since there are two edges per cycle (rising and falling), calculate the frequency
                frequency = 1 / (time_between_edges * 2)
                print(f"Frequency: {frequency:.2f} Hz")
            
            # Update last_time
            last_time = current_time
        
        # Update last_value
        last_value = value

# Simulate streaming data with a frequency of 1 ms
def listen_to_data():
    current_time = 0
    values = []
    print(os.system("pinctrl get 21"))
    current_value = parse_gpio_status( os.system("pinctrl get 21"))
    
    while True:
        values.append((current_time, current_value))
        if len(values) > 1:
            # Process the values and calculate frequency
            calculate_frequency(values)
        
        # Increment time
        current_time += UPDATE_INTERVAL
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    listen_to_data()
