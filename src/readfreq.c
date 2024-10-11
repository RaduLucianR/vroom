#include <gpiod.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define GPIO_CHIP "/dev/gpiochip4"
#define GPIO_LINE 4
#define DEBOUNCE_MS 10  // Debounce time in milliseconds

int main() {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    int64_t start_time, end_time;
    double frequency;
    int value;
    struct timespec ts;
    int prev_value = -1;
    printf("hiii");
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
    if (gpiod_line_request_input(line, "frequency_calculator") < 0) {
        perror("Failed to request GPIO line");
        gpiod_chip_close(chip);
        return 1;
    }

    // Set up timespec for time measurement
    ts.tv_sec = 0;
    ts.tv_nsec = 100000000L; // 100 ms
    printf("haaa");

    while (1) {
        // Get the current time
        clock_gettime(CLOCK_MONOTONIC, &ts);
        start_time = ts.tv_sec * 1000000000L + ts.tv_nsec;

        // Wait for the pin to change state
        do {
            value = gpiod_line_get_value(line);
            usleep(DEBOUNCE_MS * 1000);  // Debounce delay
        } while (value == prev_value);

        // Wait for the pin to change state again
        prev_value = value;
        do {
            value = gpiod_line_get_value(line);
            usleep(DEBOUNCE_MS * 1000);  // Debounce delay
        } while (value == prev_value);

        // Get the end time
        clock_gettime(CLOCK_MONOTONIC, &ts);
        end_time = ts.tv_sec * 1000000000L + ts.tv_nsec;

        // Calculate the period and frequency
        double period_ns = (double)(end_time - start_time);
        frequency = 1.0 / (period_ns / 1e9);

        // Print the frequency
        printf("Frequency: %.2f Hz\n", frequency);

        // Wait a short time before the next measurement
        usleep(10000);  // 500 ms
    }

    // Release resources
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    return 0;
}
