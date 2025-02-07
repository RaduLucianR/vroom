#ifndef VROOMWPI_H
#define VROOMWPI_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Includes
 */
#include <stdio.h>

/**
 * Macros
 */
#define VROOM_LOG(fmt, ...) printf("[VROOM] " fmt "\n", ##__VA_ARGS__)


/**
 * Constants
 */
int TRANS_PIN = 17; // Transistor Pin
int GAS_PIN = 18; // Motor/Gas Pin
int STEER_PIN = 19; // Servo/Steering Pin
int BACK_PIN = 4; // Back/Backwards Pin

/**
 * Flags
 */
static bool wiringPiInit = false;


/**
 * Functions
 */
bool initWiringPi();
void enableWheels();
void disableWheels();
void driveForwards(float value);
void driveBackwards(float value);
void forwards();
void backwards();
void steer(float value);


#ifdef __cplusplus
}
#endif

#endif //VROOMPI_H
