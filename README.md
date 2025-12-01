# AX93304_LCM Display Software

A Python-based system monitor for the Axiomtek AX93304 LCD display. This software displays real-time system information including hostname, IPv4/IPv6 addresses, CPU load, and RAM usage on a 2-line LCD screen.

## Overview

This software is designed to run on pfSense systems but is compatible with most Linux distributions. It provides a convenient way to monitor critical network and system metrics directly from the hardware LCD display panel.

## Features

- **Hostname Display** - Shows the system hostname
- **Network Monitoring** - Displays IPv4 and IPv6 addresses for both LAN and WAN interfaces
- **System Resources** - Real-time CPU load percentage and RAM usage
- **Screen Navigation** - Use arrow keys to navigate between different display pages
- **Screen Saver Mode** - Automatically cycles through pages after 10 minutes of inactivity and dims the backlight
- **Activity Detection** - Backlight restores on user interaction

## Requirements

- Python 3.x
- pySerial library
- Serial connection to the AX93304 LCD display (default: `/dev/cuau1`)
- Commands: `ifconfig`, `top`, `sysctl` (standard on pfSense and Linux)

### Installation

```bash
pip install pyserial
```

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
   - **Command**: `/usr/bin/python3 /path/to/ax93304.py &`
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

## Troubleshooting

### Display Not Updating
- Verify the serial port path is correct
- Check permissions on the serial device: `ls -la /dev/cuau1`
- Ensure the display is powered and connected

### Function Errors
- Confirm all required commands are available: `which ifconfig top sysctl`
- Check interface names match your system configuration
- Verify pySerial is installed: `python3 -c "import serial"`

### IPv6 Address Shows "N/A"
- Ensure the interface has an IPv6 address configured
- Check that it's not a link-local address (fe80::)
- Verify IPv6 is enabled on the network interface

## API Functions

The following functions are available for system monitoring:

- `getHostname()` - Returns system hostname
- `getInterfaceIpv4(interface)` - Returns IPv4 address for interface
- `getInterfaceIpv6(interface)` - Returns first non-link-local IPv6 address
- `getCpuLoad()` - Returns CPU load percentage
- `getRamUsage()` - Returns RAM usage percentage
- `backlightControl(on)` - Enable/disable display backlight
- `clearDisplay()` - Clear LCD display
- `setCursorPosition(line, position)` - Set cursor position (line 1-2, position 0-15)

## Compatibility

- **pfSense** (FreeBSD-based) - Primary target
- **Linux** - Ubuntu, Debian, CentOS, etc.
- Any system with Python 3 and standard Unix utilities

## License

See LICENSE file for details.

## Version

Current Version: 1.33.1
