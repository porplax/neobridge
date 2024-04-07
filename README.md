<p align="center">
  <img src="https://github.com/porplax/neobridge/assets/66521670/23d60ffd-23db-4962-be2c-74dc497fe5ad">
</p>

--------

<p align="center">Control your neopixels from your PC!</p>

# Installation
`pip install neobridge`
## Setup (board)
To start controlling neopixels directly from your PC, you have to setup your circuitpython board to receive serial commands. This is already programmed in the `code.py` script. Follow the steps below.
1. Download [code.py](https://github.com/porplax/neobridge/blob/master/src/neobridge/code.py)
2. Move to the circuitpython board (*RP2040 is officially supported*)
3. **You will need to edit `code.py` to fit your setup!** (*Number of LEDs, Pin location, Order*)
4. Run the script.
The script will run every bootup.

## Setup (PC/Linux/MacOS)
Now that the board is ready for serial communication, you can now control it from your PC directly. This lets you program a lot of cool lighting effects! The example below creates a 'loading' bar like effect.
```py
from itertools import cycle

from neobridge import Neobridge
import serial
import time

FRAME_RATE = 12 # How many frames per second to run code as.

# You have to provide the serial object.
a = Neobridge(serial.Serial(
            'LOCATION OF BOARD',
            baudrate=115200,
            timeout=0.05,
            write_timeout=1), 30)

# Set all LEDs to black (nothing)
a.setall((0, 0, 0))
a.show()

c = cycle(range(0, 30))
for i in c:
    a.setone((255, 255, 255), i)
    a.show()
    
    a.setall((0, 0, 0))
    time.sleep(1 / FRAME_RATE)
```
Before you can start controlling from PC, you have to enter the location of your board.
- On Windows, this is usually under a name such as `COM3`, this can be different.
- On Linux, it looks like `/dev/ttyACM0`
- On MacOS, the name looks like `/dev/tty.usbmodem1d12`


**These names can be different!**
Make sure to find the right one for the board!
## Documentation
```py
a = Neobridge(ser: serial.Serial, n_of_leds: int)
"""
Args:
        `ser (serial.Serial)`: Takes a `serial.Serial` object, this is from **pyserial**
        `n_of_leds (int)`: Number of LEDs on the board.
"""
```

```py
neobridge.wait_for_response(self)
"""
*Sends a command to the board to wait for a response.*
"""
```

```py
neobridge.setall(self, rgb: tuple)
"""
*Sets all LEDs on the board to the given RGB values.*
    Args:
        `rgb (tuple)`: RGB values to set.
"""
```

```py
neobridge.setone(self, rgb: tuple, index: int)
"""
*Sets a single LED on the board to the given RGB values.*
    Args:
        rgb (tuple): RGB values to set.
        index (int): Index of the LED to set.
"""
```

```py
neobridge.show(self)
"""
Sends a command to the board to update the LEDs.
"""
```
