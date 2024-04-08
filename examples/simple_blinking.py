import typer
import serial
import neobridge
import time

app = typer.Typer()

@app.command()
def run(port: str, number_of_leds: int, baudrate: int = 115200, timeout: float = 0.05, write_timeout: float = 1):
    FRAME_RATE = 6
    
    ser = serial.Serial(
        port,
        baudrate=baudrate,
        timeout=timeout,
        write_timeout=write_timeout)
    
    color = (0, 0, 0)
    neo = neobridge.Neobridge(ser, number_of_leds)
    neo.setall(color)
    
    neo.show()
    while True:
        if color == (0, 0, 0):
            color = (255, 255, 255)
        elif color == (255, 255, 255):
            color = (0, 0, 0)
        
        neo.setall(color)
        neo.show()
        time.sleep(1 / FRAME_RATE)
    
if __name__ == '__main__':
    typer.run(run)