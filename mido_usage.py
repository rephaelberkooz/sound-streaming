#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2013 Ole Martin Bjorndalen <ombdalen@gmail.com>
#
# SPDX-License-Identifier: MIT

"""
List available ports.

This is a simple version of mido-ports.
"""
import mido
import random
import sys
import time
from mido import Message

def print_ports(heading, port_names):
    print(heading)
    for name in port_names:
        print(f"    '{name}'")
    print()


print()
print_ports('Input Ports:', mido.get_input_names()[1])
print_ports('Output Ports:', mido.get_output_names())


if len(sys.argv) > 1:
    portname = sys.argv[1]
else:
    portname =  'loopMIDI Port 2' # Use default port

# A pentatonic scale
notes = [0, 32, 64, 92]

try:
    with mido.open_output(portname, autoreset=True) as port:
        print(f'Using {port}')
        while True:
            note = random.choice(notes)

            on = Message('control_change', control = note, channel = 1)
            print(f'Sending {on}')
            port.send(on)
            time.sleep(0.05)

except KeyboardInterrupt:
    pass