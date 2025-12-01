# AX93304_LCM Display Software

A Python-based system monitor for the Axiomtek AX93304 LCD display. This software displays real-time system information including hostname, IPv4/IPv6 addresses, CPU load, and RAM usage on a 2-line LCD screen.

## Overview

This software is designed to run on pfSense systems but is compatible with most Linux distributions. It provides a set of functions to interact with the display and can easily be forked and edited to fit most needs.

## Requirements

- Python 3.x
- pySerial library
- Serial connection to the AX93304 LCD display (default: `/dev/cuau1`)
- Commands: `ifconfig`, `top`, `sysctl` (standard on pfSense and most Linux distros)

## Configuration

Edit the configuration variables at the top of `ax93304.py`:

```python
lcmDevice = "/dev/cuau1"      # Serial device path
lanIface = "lagg0.10"          # LAN interface name
wanIface = "igb4"              # WAN interface name
```

Adjust these values according to your system's network interface names:
- On pfSense, use interface names as they appear in the web interface
- On Linux, typically `eth0`, `eth1`, `ens0`, etc.

## Usage

### Manual Execution

```bash
python3 ax93304.py
```

### pfSense Boot Configuration

To run this software automatically at boot on pfSense:

1. Install the **shellcmd** package via System > Package Manager
2. Navigate to Services > Shell Command
3. Add a new command with:
   - **Command**: `/usr/bin/python3.11 /path/to/ax93304.py &`
   - **PHP Shellcmd when** - Select your preferred timing (e.g., "Bootup")
4. Click Add and Save

Alternatively, run as a daemon process:
```bash
nohup /usr/bin/python3 /path/to/ax93304.py > /var/log/lcm_display.log 2>&1 &
```

## Display Pages

The LCD cycles through the following pages using the UP/DOWN arrow buttons:

| Page | Display |
|------|---------|
| 0 | Hostname |
| 1 | LAN IPv4 Address |
| 2 | WAN IPv4 Address |
| 3 | LAN IPv6 Address |
| 4 | WAN IPv6 Address |
| 5 | CPU Load & RAM Usage |

### Navigation Controls

- **UP/DOWN** - Change display page
- **LEFT/RIGHT** - Scroll horizontally (for longer text)

## Hardware Connection

Connect the AX93304 LCD display to the system via serial connection:

- Default serial device: `/dev/cuau1` (pfSense/FreeBSD)
- Baud rate: 9600
- Timeout: 1 second

Adjust the `lcmDevice` variable if using a different serial port.

## API Functions

The following functions are available:

- `getHostname()` - Returns system hostname
- `getInterfaceIpv4(interface)` - Returns IPv4 address for interface
- `getInterfaceIpv6(interface)` - Returns first non-link-local IPv6 address
- `getCpuLoad()` - Returns CPU load percentage
- `getRamUsage()` - Returns RAM usage percentage
- `backlightControl(on)` - Enable/disable display backlight
- `clearDisplay()` - Clear LCD display
- `setCursorPosition(line, position)` - Set cursor position (line 1-2, position 0-15)

## Version

Current Version: 1.33.1
