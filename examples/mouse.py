import typer
import serial
import neobridge
import pyautogui
import time

app = typer.Typer()

@app.command()
def run(port: str, number_of_leds: int, baudrate: int = 115200, timeout: float = 0.05, write_timeout: float = 1):
    ser = serial.Serial(
        port,
        baudrate=baudrate,
        timeout=timeout,
        write_timeout=write_timeout)
    neo = neobridge.Neobridge(ser, number_of_leds)
    OFFSET = -1

    while True:
        x, y = pyautogui.position()
        x = int(x/64)
        neo.setall((255, 0, 0))
        
        brightness = (int(y/30)*-1)*5
        # has to be a better way of doing this 💀
        try:
            neo.setone((64+min(brightness, 64), 64+min(brightness, 64), 64+min(brightness, 64)), x-(2-OFFSET))
            neo.setone((127+min(min(brightness, 127), 127), 127+min(brightness, 127), 127+min(brightness, 127)), x-(1-OFFSET))
            neo.setone((255+min(brightness, 255), 255+min(brightness, 255), 255+min(brightness, 255)), x+(OFFSET))
            neo.setone((127+min(brightness, 127), 127+min(brightness, 127), 127+min(brightness, 127)), x+(1+OFFSET))
            neo.setone((64+min(brightness, 64), 64+min(brightness, 64), 64+min(brightness, 64)), x+(2+OFFSET))
        except IndexError:
            pass
        
        neo.show()
        time.sleep(0.0010)

if __name__ == '__main__':
    typer.run(run)
    
