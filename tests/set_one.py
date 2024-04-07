from itertools import cycle

import neobridge.neobridge as n
import serial
import time

FRAME_RATE = 12

a = n.Neobridge(serial.Serial(
            'COM3',
            baudrate=115200,
            timeout=0.05,
            write_timeout=1), 30)
a.setall((0, 0, 0))

c = cycle(range(0, 30))
for i in c:
    a.setone((255, 255, 255), i)
    a.show()
    
    a.setall((0, 0, 0))
    time.sleep(1 / FRAME_RATE)