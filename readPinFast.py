import gpiod
import time

def measure_frequency(pin, duration=1):
    # Create a chip object for the GPIO chip (usually gpiochip0)
    chip = gpiod.Chip('gpiochip4')
    
    # Get the line object for the specified GPIO pin
    line = chip.get_line(pin)
    
    # Request the line for input with edge detection on both rising and falling edges
    line.request(consumer='freq_measurer', type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    start_time = time.time()
    edge_count = 0

    # Monitor for edges for the specified duration
    while time.time() - start_time < duration:
        event = line.event_wait(timeout_ms=1000)  # Wait for an event with a timeout
        if event:
            edge_count += 1
    
    # Release the line and cleanup
    line.release()
    chip.close()
    
    # Calculate the frequency
    elapsed_time = time.time() - start_time
    frequency = edge_count / (2 * elapsed_time)  # Each edge is half a cycle
    return frequency

# Example usage
pin = 4  # Replace with your GPIO pin number
duration = 0.001  # Measurement duration in seconds
frequency = measure_frequency(pin, duration)
print(f"Frequency: {frequency} Hz")
