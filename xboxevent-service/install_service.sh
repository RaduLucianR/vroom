#!/bin/bash

cp ./xboxevent.service /etc/systemd/system/xboxevent.service
sudo systemctl daemon-reload
sudo systemctl start xboxevent
sudo systemctl enable xboxevent
