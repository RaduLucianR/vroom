#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2023 Kent Gibson <warthog618@gmail.com>

"""Minimal example of reading a single line."""

import time
import gpiod

from gpiod.line import Direction


def get_line_value(chip_path, line_offset):
    with gpiod.request_lines(
        chip_path,
        consumer="get-line-value",
        config={line_offset: gpiod.LineSettings(direction=Direction.INPUT)},
    ) as request:
        value = request.get_value(line_offset)
        print("{}={}".format(line_offset, value))

try:
    for i in range(1,1,1000):
        get_line_value("/dev/gpiochip4")
        print('HI')
        time.sleep(0.001)
except OSError as ex:
    print(ex, "\nCustomise the example configuration to suit your situation")
