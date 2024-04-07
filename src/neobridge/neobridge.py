import json
import sys
import time
import serial
try:
    from neopixel import NeoPixel
except ModuleNotFoundError:
    NeoPixel = None
import supervisor
from neobridge.command import Command

class Neobridge:
    def __init__(self, ser: serial.Serial, n_of_leds: int):
        self.MAXIMUM_LEDS = n_of_leds-1
        
        self.ser = ser     
        self.ser.reset_input_buffer()
    
    def _send_cmd(self, cmd: str):
        self.ser.write(bytes(json.dumps(cmd).encode()))
        self.ser.write(b"\r\n")
        self.ser.flush()
    
    def _reset(self):
        """Resets the board. Useful if you want to reset the board to a known state.
        """
        self._send_cmd({'command': Command.RESET.value})
    
    def wait_for_response(self):
        """Sends a command to the board to wait for a response.
        """
        self._send_cmd({'command': Command.WAIT_FOR_RESPONSE.value})
        size = None
        while not size:
            size = self.ser.inWaiting()
    
    def setall(self, rgb: tuple):
        """Sets all LEDs on the board to the given RGB values.

        Args:
            rgb (tuple): RGB values to set.
        """
        self._send_cmd({'command': Command.SET_ALL.value, 'r': rgb[0], 'g': rgb[1], 'b': rgb[2]})
    
    def setone(self, rgb: tuple, index: int):
        """Sets a single LED on the board to the given RGB values.

        Args:
            rgb (tuple): RGB values to set.
            index (int): Index of the LED to set.
        """
        if index > self.MAXIMUM_LEDS:
            raise IndexError("Index out of range")
        self._send_cmd({'command': Command.SET_ONE.value, 'r': rgb[0], 'g': rgb[1], 'b': rgb[2], 'index': index})
    
    def show(self):
        """Sends a command to the board to update the LEDs.
        """
        self._send_cmd({'command': Command.SHOW.value})
        
    def run(self, neo: NeoPixel, rate: int = 12):
        """Runs the NeoPixel program on the board.
        
            Args:
                neopixel (neopixel.NeoPixel): The NeoPixel object to use.
                rate (int, optional): The rate at which to update the LEDs. Defaults to 12
                """
        stdin = sys.stdin
        while True:
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
                    
                    if command == Command.WAIT_FOR_RESPONSE.value:
                        print('\r\n')
                    elif command == Command.SET_ALL.value:
                        r,g,b = data['r'],data['g'],data['b']
                        neo.fill((r,g,b))
                    elif command == Command.SET_ONE.value:
                        r,g,b = data['r'],data['g'],data['b']
                        i = data['index']
                        neo[i] = (r,g,b)
                    elif command == Command.SHOW.value:
                        neo.show()
                    elif command == Command.RESET.value:
                        print('\r\n')
                        supervisor.reload()
                except:
                    pass
            time.sleep(1 / rate)