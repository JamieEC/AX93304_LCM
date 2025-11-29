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

def clearDisplay():
    lcmSerial.write(b'\xFE\x01')  # Command to clear display

def displayControl(on):
    if on:
        lcmSerial.write(b'\xFE\x0C')  # Command to turn display on
    else:
        lcmSerial.write(b'\xFE\x08')  # Command to turn display off

def shiftCursorLeft():
    lcmSerial.write(b'\xFE\x10')  # Command to shift cursor left

def shiftCursorRight():
    lcmSerial.write(b'\xFE\x14')  # Command to shift cursor right

def setCursorPosition(line, position):
    if line == 1:
        cmd = 0x80 + position
    elif line == 2:
        cmd = 0xC0 + position
    lcmSerial.write(bytes([0xFE, cmd]))  # Command to set cursor position
    
backlightControl(True)  # Turn backlight on
homePosition()         # Move to home position
lcmSerial.write("Hello, World!".encode('utf-8'))  # Send text to display
setCursorPosition(2, 0)  # Move cursor to line 2, position 0
lcmSerial.write("Line 2 Text".encode('utf-8'))  # Send text to line 2
lcmSerial.close()  # Close the serial connection

