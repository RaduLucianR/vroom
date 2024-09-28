#!/bin/bash

cp ./motor.service /etc/systemd/system/motor.service
sudo systemctl daemon-reload
sudo systemctl start motor
sudo systemctl enable motor
