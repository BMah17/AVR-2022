import time

import serial


class SerialLoop(serial.Serial):
    """
    Like the normal pyserial class, but with a method to run forever.
    """

    def run(self) -> None:
        while True:
            while self.in_waiting > 0:
                self.read(1)
            time.sleep(0.01)
