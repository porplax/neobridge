import neopixel
import supervisor
import board
import sys
import time
import json
RESET = -2
WAIT_FOR_RESPONSE = -1
SET_ALL = 0
SET_ONE = 1
SHOW = 2

PIXEL_PIN = board.GP15
NUMBER_OF_PIXELS = 30
ORDER = neopixel.GRB

neo = neopixel.NeoPixel(
    PIXEL_PIN, NUMBER_OF_PIXELS, brightness=1, auto_write=False, pixel_order=ORDER)
neo.fill((0, 0, 0))
neo.show()

serial = sys.stdin

while True:
    if supervisor.runtime.serial_bytes_available:
        data_in = serial.readline()
        data = None
        if data_in:
            try:
                data = json.loads(data_in)
            except ValueError:
                data = {"raw": data_in}

        if isinstance(data, dict):
            try:
                command = data['command']
                
                if command == WAIT_FOR_RESPONSE:
                    print('\r\n')
                elif command == SET_ALL:
                    r,g,b = data['r'],data['g'],data['b']
                    neo.fill((r,g,b))
                elif command == SET_ONE:
                    r,g,b = data['r'],data['g'],data['b']
                    i = data['index']
                    neo[i] = (r,g,b)
                elif command == SHOW:
                    neo.show()
                elif command == RESET:
                    print('\r\n')
                    supervisor.reload()
            except:
                pass
                    
                    
    time.sleep(0.0001)
