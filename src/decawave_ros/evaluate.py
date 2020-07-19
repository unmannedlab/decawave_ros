#!/usr/bin/env python3

import time
import serial
import numpy as np 
from decawave_ros import DecaParser

t0a0 = np.array([])
t0a1 = np.array([])
t1a0 = np.array([])
t1a1 = np.array([])
i = 0

try:
    port = serial.Serial(
        port        = '/dev/ttyACM0',
        baudrate    = 9600,
        timeout     = 10
    )
except serial.SerialException:
    print("Serial Port Connection Failure")

time_start = time.time()
parser = DecaParser(port)
while (i<100):
    try:
        msg = parser.receive()
        if(msg):
            if(msg.tag==0):
                t0a0 = np.append(t0a0, msg.r0)
                t0a1 = np.append(t0a1, msg.r1)
            if(msg.tag==1):
                t1a0 = np.append(t1a0, msg.r0)
                t1a1 = np.append(t1a1, msg.r1)
            i = i + 1
    except (ValueError, IOError) as err:
        print(err)

time_end = time.time()

print('Average Rate: ' + '{:.4}'.format(float(i) / 2 / (time_end - time_start) ) + ' Hz')
print('t0->a0:   Mean: ' + '{:.4}'.format(np.mean(t0a0)) + ' \tStdDev: ' + '{:.3}'.format(np.std(t0a0)))
print('t0->a1:   Mean: ' + '{:.4}'.format(np.mean(t0a1)) + ' \tStdDev: ' + '{:.3}'.format(np.std(t0a1)))
print('t1->a0:   Mean: ' + '{:.4}'.format(np.mean(t1a0)) + ' \tStdDev: ' + '{:.3}'.format(np.std(t1a0)))
print('t1->a1:   Mean: ' + '{:.4}'.format(np.mean(t1a1)) + ' \tStdDev: ' + '{:.3}'.format(np.std(t1a1)))