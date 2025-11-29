#Version 1.0
import serial
import socket

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
    # line: 1 or 2, position: 0-15
    if line == 1:
        cmd = 0x80 + position
    elif line == 2:
        cmd = 0xC0 + position
    lcmSerial.write(bytes([0xFE, cmd]))  # Command to set cursor position
    
def getHostname():
    return socket.gethostname()

def getInterfaceIp(interface):
    return "192.168.0.1"

def initDisplay():
    backlightControl(True)
    clearDisplay()
    homePosition()

initDisplay()

page = 1

match page:
    case 0:
        lcmSerial.write("HOST:".encode('utf-8'))  # Send text to display
        setCursorPosition(2, 0)  # Move cursor to line 2, position 0
        lcmSerial.write(getHostname().encode('utf-8'))  # Send text to line 2
    case 1:
        lcmSerial.write(f"LAN IP:{getInterfaceIp("eth0")}".encode('utf-8'))  # Send text to display
        setCursorPosition(2, 0)  # Move cursor to line 2, position 0
        lcmSerial.write(f"WAN IP:{getInterfaceIp("eth0")}".encode('utf-8'))  # Send text to display
    case 2:
        page = 0  # Reset page to 0
        

lcmSerial.close()  # Close the serial connection