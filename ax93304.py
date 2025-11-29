import serial

lcmDevice = "/dev/cuau1"

lcmSerial = serial.Serial(lcmDevice, baudrate=9600, timeout=1)

def backlightControl(on):
    if on:
        lcmSerial.write(b'\xFB')  # Command to turn backlight on
    else:
        lcmSerial.write(b'\xFC')  # Command to turn backlight off

while True:
    backlightControl(True)  # Turn backlight on
    # wait for 1 second
    import time
    time.sleep(1)
    backlightControl(False)  # Turn backlight off
    time.sleep(1)
