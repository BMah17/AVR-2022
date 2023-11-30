import contextlib
import glob
import sys
from typing import List

import serial


def list_serial_ports() -> List[str]:
    """
    Returns a list of serial ports on the system.
    """
    if sys.platform.startswith("win"):
        ports = [f"COM{i + 1}" for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        with contextlib.suppress(OSError, serial.SerialException):
            s = serial.Serial(port)
            s.close()
            result.append(port)
    return result
