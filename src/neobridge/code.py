import neopixel
import supervisor
import board
import sys
import time
import json

class Command:
    SHOW = -3
    RESET = -2
    WAIT_FOR_RESPONSE = -1

    SET_ALL = 0
    SET_ONE = 1
    SET_TO_LIST = 2

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
                
                if command == Command.SHOW:
                    neo.show()
                elif command == Command.RESET:
                    print('\r\n')
                    supervisor.reload()
                elif command == Command.WAIT_FOR_RESPONSE:
                    print('\r\n')
                elif command == Command.SET_ALL:
                    r,g,b = data['r'],data['g'],data['b']
                    neo.fill((r,g,b))
                elif command == Command.SET_ONE:
                    r,g,b = data['r'],data['g'],data['b']
                    i = data['index']
                    neo[i] = (r,g,b)
                elif command == Command.SET_TO_LIST:
                    _list = data['rgb_list']
                    for i in range(len(neo)):
                        neo[i] = _list[i]
            except:
                pass