import serial

lcmDevice = "/dev/cuau1"

lcmSerial = serial.Serial(lcmDevice, baudrate=9600, timeout=1)

def backlightControl(on):
    if on:
        lcmSerial.write(b'\xFB')  # Command to turn backlight on
    else:
        lcmSerial.write(b'\xFC')  # Command to turn backlight off

def homePosition():
    lcmSerial.write(b'\xFE\x02')  # Command to move to home position


backlightControl(True)  # Turn backlight on
homePosition()         # Move to home position
lcmSerial.write("Hello, World!".encode('utf-8'))  # Send text to display
lcmSerial.close()  # Close the serial connection

