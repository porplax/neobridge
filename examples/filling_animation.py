import time
import random
import typer
import serial
import neobridge

app = typer.Typer()

@app.command()
def run(port: str, number_of_leds: int, baudrate: int = 115200, timeout: float = 0.05, write_timeout: float = 1):
    ser = serial.Serial(
        port,
        baudrate=baudrate,
        timeout=timeout,
        write_timeout=write_timeout)
    neo = neobridge.Neobridge(ser, number_of_leds)
    
    FRAME_RATE = 30
    
    color = (255, 0, 0)
    neo.show()
    while True:
        for i in range(number_of_leds):
            neo.setone(color, i)
            neo.show()
            time.sleep(1 / FRAME_RATE)
    
        r,g,b = random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)
        color = (r, g, b)
        time.sleep(1 / FRAME_RATE)
    
    
    
if __name__ == '__main__':
    typer.run(run)