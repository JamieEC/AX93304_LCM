#Version 1.32.4
import serial
import socket
import subprocess
import re
import time

lcmDevice = "/dev/cuau1"
lcmSerial = serial.Serial(lcmDevice, baudrate=9600, timeout=1)

lanIface = "lagg0.10"
wanIface = "igb4"

def backlightControl(on):
    if on:
        lcmSerial.write(b'\xFB')  # Command to turn backlight on
    else:
        lcmSerial.write(b'\xFC')  # Command to turn backlight off

def homePosition():
    print("Moving cursor to home position...")
    lcmSerial.write(b'\xFE\x02')  # Command to move to home position

def clearDisplay():
    print("Clearing display...")
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

def getInterfaceIpv4(interface):
    try:
        result = subprocess.run(['ifconfig', interface], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parse the output to find the IPv4 address
            match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', result.stdout)
            if match:
                return match.group(1)
        return "N/A"
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Error getting IP for {interface}: {e}")
        return "N/A"

def getInterfaceIpv6(interface):
    try:
        result = subprocess.run(['ifconfig', interface], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parse the output to find IPv6 addresses (excluding link-local)
            matches = re.findall(r'inet6\s+([a-f0-9:]+)', result.stdout)
            for ipv6 in matches:
                # Skip link-local addresses (start with fe80)
                if not ipv6.lower().startswith('fe80'):
                    return ipv6
        return "N/A"
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Error getting IPv6 for {interface}: {e}")
        return "N/A"

def getCpuLoad():
    try:
        result = subprocess.run(['top', '-bn'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parse the output to find CPU usage
            match = re.search(r'CPU:\s+(\d+\.\d+)%\s+user', result.stdout)
            if match:
                return match.group(1) + "%"
        return "N/A"
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Error getting CPU load: {e}")
        return "N/A"

def getRamUsage():
    try:
        result = subprocess.run(['sysctl', 'hw.physmem', 'vm.stats.vm.v_page_count', 'vm.stats.vm.v_free_count'], 
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parse sysctl output for memory info
            physmem_match = re.search(r'hw\.physmem:\s+(\d+)', result.stdout)
            free_match = re.search(r'vm\.stats\.vm\.v_free_count:\s+(\d+)', result.stdout)
            total_match = re.search(r'vm\.stats\.vm\.v_page_count:\s+(\d+)', result.stdout)
            
            if physmem_match and total_match and free_match:
                total_pages = int(total_match.group(1))
                free_pages = int(free_match.group(1))
                used_pages = total_pages - free_pages
                ram_percent = (used_pages / total_pages) * 100
                return f"{ram_percent:.1f}%"
        return "N/A"
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Error getting RAM usage: {e}")
        return "N/A"

def initDisplay():
    #backlightControl(True)
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
        activity = True
        position = shiftDisplayRight(position)
        print(f"Current position: {position}")
    elif serialData == b'\x4E':  # If 'LEFT' key is pressed
        print("LEFT key pressed")
        activity = True
        position = shiftDisplayLeft(position)
        print(f"Current position: {position}")
    elif serialData == b'\x4D':  # If 'UP' key is pressed
        activity = True
        #print("UP key pressed")
        while lcmSerial.read() != b'O':
            print("Wait")
        #print("Up Key released")
        page += 1
        initDisplay()
        position = 0
        print(f"Current page: {page}")
    elif serialData == b'\x4B':  # If 'DOWN' key is pressed
        activity = True
        print("DOWN key pressed")
        while lcmSerial.read() != b'O':
            print("Wait")
        print("Down Key released")
        page -= 1
        initDisplay()
        position = 0
        print(f"Current page: {page}")
    else:
        activity = False
    return page, position, activity

displayControl(True)
initDisplay()
backlightControl(True)

page = 0
position = 0

# print("LAN Interface IPv4:", getInterfaceIpv4(lanIface))
# print("WAN Interface IPv4:", getInterfaceIpv4(wanIface))

# print("LAN Interface IPv6:", getInterfaceIpv6(lanIface))
# print("WAN Interface IPv6:", getInterfaceIpv6(wanIface))

print("CPU Load:", getCpuLoad())
print("RAM Usage:", getRamUsage())

print("Starting main loop...")

lastActivityTime = time.time()
screenSaverTime = time.time()

activity = False
screenSaverMode = False

while True:

    currentTime = time.time()
    if activity:
        backlightControl(True)
        lastActivityTime = currentTime
        screenSaverMode = False
    elif currentTime - lastActivityTime > 60:
        print("Entering screen saver mode...")
        screenSaverMode = True
        #backlightControl(False)

    if screenSaverMode:
        if currentTime - screenSaverTime > 10:
            page += 1
            print(f"Screen saver changing to page: {page}")
            screenSaverTime = currentTime

    match page:
        case 0:
            setCursorPosition(1, 0)
            #print("Moved cursor to line 1")
            lcmSerial.write("Hostname".encode('utf-8'))  # Send text to display
            setCursorPosition(2, 0)  # Move cursor to line 2, position 0
            #print("Moved cursor to line 2")
            lcmSerial.write(getHostname().encode('utf-8'))  # Send text to line 2
        case 1:
            setCursorPosition(1, 0)
            lcmSerial.write("LAN IPv4".encode('utf-8'))  # Send text to display
            setCursorPosition(2, 0)  # Move cursor to line 2, position 0
            lcmSerial.write(getInterfaceIpv4(lanIface).encode('utf-8'))  # Send text to display
        case 2:
            setCursorPosition(1, 0)
            lcmSerial.write("WAN IPv4".encode('utf-8'))  # Send text to display
            setCursorPosition(2, 0)  # Move cursor to line 2, position 0
            lcmSerial.write(getInterfaceIpv4(wanIface).encode('utf-8'))  # Send text to display
        case 3:
            setCursorPosition(1, 0)
            lcmSerial.write("LAN IPv6".encode('utf-8'))  # Send text to display
            setCursorPosition(2, 0)  # Move cursor to line 2, position 0
            lcmSerial.write(getInterfaceIpv6(lanIface).encode('utf-8'))  # Send text to display
        case 4:
            setCursorPosition(1, 0)
            lcmSerial.write("WAN IPv6".encode('utf-8'))  # Send text to display
            setCursorPosition(2, 0)  # Move cursor to line 2, position 0
            lcmSerial.write(getInterfaceIpv6(wanIface).encode('utf-8'))  # Send text to display
        case 5:
            setCursorPosition(1, 0)
            lcmSerial.write(("CPU" + getCpuLoad()).encode('utf-8'))  # Send text to display
            setCursorPosition(2, 0)  # Move cursor to line 2, position 0
            lcmSerial.write(("RAM" + getRamUsage()).encode('utf-8'))  # Send text to display
        case -1:
            page = 5 
            print("Invalid page")
        case 6:
            page = 0
            print("Invalid page")


    page, position, activity = readButtons(page, position)