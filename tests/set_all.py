import neobridge.neobridge as n
import serial

a = n.Neobridge(serial.Serial(
            'COM3',
            baudrate=115200,
            timeout=0.05,
            write_timeout=1), 30)

for i in range(255):
    a.setall((i, i, i))
    a.show()