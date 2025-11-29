#Version 1.8
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
    return "192.168.100.200"  # Placeholder for actual IP retrieval

def initDisplay():
    backlightControl(True)
    clearDisplay()
    homePosition()

def shiftDisplayLeft(position):
    if position < 15:
        position += 1
        lcmSerial.write(b'\xFE\x18')  # Command to shift display left
    return position

def shiftDisplayRight(position):
    if position > 0:
        lcmSerial.write(b'\xFE\x1C')  # Command to shift display right
        position -= 1
    return position

def readButtons(page, position):
    lcmSerial.write(b'\xFD')  # Keypad listen mode 
    serialData = lcmSerial.read()
    # print(serialData) # debugging line
    if serialData == b'\x47':  # If 'RIGHT' key is pressed
        print("RIGHT key pressed")
        position = shiftDisplayRight(position)
    elif serialData == b'\x4E':  # If 'LEFT' key is pressed
        print("LEFT key pressed")
        position = shiftDisplayLeft(position)
    elif serialData == b'\x4D':  # If 'UP' key is pressed
        print("UP key pressed")
        page += 1
        clearDisplay()
        position = 0
        print(f"Current page: {page}")
    elif serialData == b'\x4B':  # If 'DOWN' key is pressed
        print("DOWN key pressed")
        page -= 1
        clearDisplay
        position = 0
        print(f"Current page: {page}")
    return page, position

initDisplay()
page = 0
position = 0

while True:
    match page:
        case 0:
            #clearDisplay()
            lcmSerial.write("sHOST:".encode('utf-8'))  # Send text to display
            setCursorPosition(2, 0)  # Move cursor to line 2, position 0
            lcmSerial.write(getHostname().encode('utf-8'))  # Send text to line 2
        case 1:
            #clearDisplay()
            lanIface = "eth0"
            wanIface = "eth0"
            lcmSerial.write(f"sLAN:{getInterfaceIp(lanIface)}".encode('utf-8'))  # Send text to display
            setCursorPosition(2, 0)  # Move cursor to line 2, position 0
            lcmSerial.write(f"WAN:{getInterfaceIp(wanIface)}".encode('utf-8'))  # Send text to display
        case 2:
            page = 1
        case -1:
            page = 0 

    page, position = readButtons(page, position)