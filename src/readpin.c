#include <gpiod.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#define GPIO_CHIP "/dev/gpiochip4"
#define GPIO_LINE 3  // Replace with the GPIO line number you are using
#define INTERVAL_US 1000  // 10 microseconds

int main() {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    int value;
    struct timespec start_time, end_time;
    double elapsed_time;

    // Open GPIO chip
    chip = gpiod_chip_open(GPIO_CHIP);
    if (!chip) {
        perror("Failed to open GPIO chip");
        return 1;
    }

    // Get GPIO line
    line = gpiod_chip_get_line(chip, GPIO_LINE);
    if (!line) {
        perror("Failed to get GPIO line");
        gpiod_chip_close(chip);
        return 1;
    }

    // Request line as input
    if (gpiod_line_request_input(line, "read_value") < 0) {
        perror("Failed to request GPIO line as input");
        gpiod_chip_close(chip);
        return 1;
    }

    // Main loop
    while (1) {
        // Get the current time
        clock_gettime(CLOCK_MONOTONIC, &start_time);

        // Read GPIO line value
        value = gpiod_line_get_value(line);
        if (value < 0) {
            perror("Failed to read GPIO line value");
        } else {
            printf("GPIO line value: %d\n", value);
        }

        // Sleep for the specified interval
        usleep(INTERVAL_US);

        // Optionally, measure and print the actual elapsed time for debugging
        clock_gettime(CLOCK_MONOTONIC, &end_time);
        elapsed_time = (end_time.tv_sec - start_time.tv_sec) * 1e6;
        elapsed_time += (end_time.tv_nsec - start_time.tv_nsec) / 1e3;
        printf("Elapsed time: %.2f microseconds\n", elapsed_time);
    }

    // Release resources
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    return 0;
}
