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
```rust
use neobridge_rust::{Neobridge, RGB};

fn main() {
    let mut neobridge = Neobridge::new("COM3", 30);
    neobridge.set_all(RGB(0, 0, 0));
    neobridge.show();

    let mut i = 0;
    loop {
        if (i == 30) {
            i = 0;
        }

        neobridge.set_one(RGB(255, 255, 255), i);
        neobridge.show();
        std::thread::sleep(std::time::Duration::from_millis(50));

        neobridge.set_all(RGB(0, 0, 0));

        i += 1;
    }
}
```
Before you can start controlling from PC, you have to enter the location of your board.
- On Windows, this is usually under a name such as `COM3`, this can be different.
- On Linux, it looks like `/dev/ttyACM0`
- On MacOS, the name looks like `/dev/tty.usbmodem1d12`


**These names can be different!**
Make sure to find the right one for the board!
## Documentation
```rust
let neobridge = Neobridge::new("COM3", 30);
/*
*Connects to the board and initializes a struct object.*
Args:
        `port (str)`: Takes a `str` object to initialize the board.
        `n_of_leds (u32)`: Number of LEDs on the board.
*/
```

```rust
neobridge.set_all(self, rgb: RGB)
/*
*Sets all LEDs on the board to the given RGB values.*
    Args:
        `rgb (RGB)`: RGB values to set.
*/
```

```rust
neobridge.set_one(self, rgb: RGB, index: u32)
/*
*Sets a single LED on the board to the given RGB values.*
    Args:
        rgb (RGB): RGB values to set.
        index (u32): Index of the LED to set.
*/
```

```rust
neobridge.set_list(self, rgb_list: Vec<RGB>)
/*
*Gives the board a list of RGB values to set.*
    Args:
        rgb_list (Vec<RGB>): RGB list to set.
*/
```

```rust
neobridge.show(self)
/*
Sends a command to the board to update the LEDs.
*/
```
# TO-DO List
- [X] Create automated installer for the board.
