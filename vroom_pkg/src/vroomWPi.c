#include <stdbool.h>
#include <stdio.h>

#include <wiringPi.h>

#include "vroomWPi.h"

bool initWiringPi() {
	if (wiringPiInit == false) {
		wiringPiSetupGpio();		
		wiringPiInit = true;
	}
	
	return true;
}

void enableWheels() {
	if (wiringPiInit == false) {
		printf("enableWheels(): WiringPi is not initialized!\n");
		return;
	}
	
    pinMode(TRANS_PIN, OUTPUT);
    digitalWrite(TRANS_PIN, HIGH);
    VROOM_LOG("Wheel movement enabled!");
}

void disableWheels() {
	if (wiringPiInit == false) {
		printf("disableWheels(): WiringPi is not initialized!\n");
		return;
	}
	
	wiringPiSetupGpio(); 
    pinMode(TRANS_PIN, OUTPUT);
    digitalWrite(TRANS_PIN, LOW);
    VROOM_LOG("Wheel movement disabled!");
}

void driveForwards(float value) {
	pinMode(BACK_PIN, OUTPUT);
    pinMode(GAS_PIN, PWM_OUTPUT);

    digitalWrite(BACK_PIN, LOW); // Set BACKWARDS_PIN to LOW
    pwmSetRange(100);
    pwmWrite(GAS_PIN, (int) value);     // Set PWM value for GAS_PIN
}

void driveBackwards(float value) {
	pinMode(BACK_PIN, OUTPUT);
    pinMode(GAS_PIN, PWM_OUTPUT);

    digitalWrite(BACK_PIN, HIGH); // Set BACKWARDS_PIN to HIGH
    pwmSetRange(100);
    pwmWrite(GAS_PIN, (int) value);     // Set PWM value for GAS_PIN
}

void steer(float value) {
    pinMode(STEER_PIN, PWM_OUTPUT);

    pwmSetRange(1024);
    pwmWrite(STEER_PIN, (int) value);     // Set PWM value for GAS_PIN
}

void forwards() {
	pinMode(BACK_PIN, OUTPUT);
    digitalWrite(BACK_PIN, LOW); // Set BACKWARDS_PIN to HIGH
}

void backwards() {
	pinMode(BACK_PIN, OUTPUT);
    digitalWrite(BACK_PIN, HIGH); // Set BACKWARDS_PIN to HIGH
}
