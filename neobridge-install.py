import os
import win32api
import tempfile
import requests
import shutil
import time

os.system("cls")

title = """
█░█ █▀▀ ▀█   █░█ ▀█▀ █ █░░ █ ▀█▀ █▄█
█▄█ █▀░ █▄   █▄█ ░█░ █ █▄▄ █ ░█░ ░█░
@porplax
=============>"""

print("Neobridge UF2 Utility | Easy installation")
print(title)
print("assuming user has board in BOOTSEL...")

cur = None

def find_drive_by_name(name: str):
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    driveNames = [win32api.GetVolumeInformation(x) for x in drives]
    for count, n in enumerate(driveNames):
        if n[0] == name:
            return drives[count]

def wait_until_drive_by_name(name: str):
    time.sleep(1)
    for _i in range(0, 50):
        drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        driveNames = [win32api.GetVolumeInformation(x) for x in drives]
        
        for n in driveNames:
            if n[0] == name:
                return True
        time.sleep(1)
    return False

cur = find_drive_by_name('RPI-RP2')

if cur == None:
    print("couldn't find board. Put it into BOOT-SEL, abort...")
    exit()
else:
    print(f'found RPI-RP2 as {cur}')

confirm = input("\u001b[31mWARNING: this WILL delete everything off your board, proceed?\n(y/n)>\u001b[0m ")
if confirm == "y":
    pass
else:
    print("abort.")
    exit()

os.system("cls")

board = int(input("1: Pico/2: Pico W ?> "))
dir = tempfile.TemporaryDirectory()

print(f"nuking {cur}...")
r = requests.get("https://github.com/dwelch67/raspberrypi-pico/raw/main/flash_nuke.uf2")
fname = dir.name + rf"\flash_nuke.uf2"
open(fname, 'wb').write(r.content)
shutil.move(fname, cur)

wait_until_drive_by_name("RPI-RP2")

uf2 = "adafruit-circuitpython-raspberry_pi_pico-en_US-9.0.5.uf2" if board == 1 else "adafruit-circuitpython-raspberry_pi_pico_w-en_US-9.0.5.uf2"
fname = dir.name + rf"\{uf2}" if board == 1 else dir.name + rf"\{uf2}"
url = f"https://downloads.circuitpython.org/bin/raspberry_pi_pico/en_US/{uf2}" if board == 1 else f"https://downloads.circuitpython.org/bin/raspberry_pi_pico_w/en_US/{uf2}"

print(uf2)
print(fname)
print(f"downloading .UF2 for {url}")
r = requests.get(url)
open(fname , 'wb').write(r.content)

print(f"flashing .UF2 into {cur}")
shutil.move(fname, cur)

wait_until_drive_by_name("CIRCUITPY")
cur = find_drive_by_name("CIRCUITPY")
os.system("cls")

print("Enter information like which pin the NeoPixel is connected, order, number of pixels, etc...")
pin = int(input("Pin number (Layout)> "))
n_of_pixels = int(input("Number of pixels (LEDs on the NeoPixel)> "))
order = input("Order (GRB, or other)> ")

print("downloading latest version of neobridge...")
neobridge = dir.name + rf'\code.py'
r = requests.get("https://github.com/porplax/neobridge/raw/master/src/neobridge/code.py")

code = r.content.decode("utf-8")
code = code.replace("PIXEL_PIN = board.GP15", f"PIXEL_PIN = board.GP{pin}")
code = code.replace("NUMBER_OF_PIXELS = 30", f"NUMBER_OF_PIXELS = {n_of_pixels}")
code = code.replace("ORDER = neopixel.GRB", f"ORDER = neopixel.{order.upper()}")

open(neobridge, 'w').write(code)
    
print("downloading latest version of neopixel...")
neopixel = dir.name + rf"\CircuitPython_NeoPixel.zip"
r = requests.get("https://learn.adafruit.com/elements/2984640/download?type=zip")
open(neopixel, 'wb').write(r.content)

print("extracting bundle...")
shutil.unpack_archive(neopixel, dir.name + r"\bundle")
neopixel = dir.name + r"\bundle"

print(f"moving code.py to {cur}")
os.remove(cur+"code.py")
shutil.move(neobridge, cur)

print(rf"moving neopixel.mpy to {cur}lib")
shutil.move(rf"{neopixel}\CircuitPython_Essentials\CircuitPython_NeoPixel\CircuitPython 9.x\lib\neopixel.mpy", cur + r"\lib")

dir.cleanup()
os.system('cls')
print("Finished, your board will now run neobridge on boot!")
print("If it is not working, check thonny for output logs.")