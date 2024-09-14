#include <gpiod.h>
#include <stdio.h>

#define GPIO_CHIP "/dev/gpiochip4"
#define GPIO_LINE 4

int main() {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    int value;

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
    if (gpiod_line_request_input(line, "my_program") < 0) {
        perror("Failed to request GPIO line");
        gpiod_chip_close(chip);
        return 1;
    }

    // Read value
    value = gpiod_line_get_value(line);
    if (value < 0) {
        perror("Failed to read GPIO line value");
    } else {
        printf("GPIO line value: %d\n", value);
    }

    // Release resources
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    return 0;
}


