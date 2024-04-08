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
    
if __name__ == '__main__':
    typer.run(run)