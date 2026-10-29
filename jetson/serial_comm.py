# ============================================================
# serial_comm.py
# Handles USB Serial communication between
# Jetson Nano (Python) and Arduino Uno
# ============================================================

import serial
import time
from config import SERIAL_PORT, BAUD_RATE


class SerialComm:

    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset after serial connect
            print(f"Serial connected on {SERIAL_PORT} at {BAUD_RATE} baud.")
        except serial.SerialException as e:
            raise RuntimeError(f"Could not open serial port {SERIAL_PORT}.\nError: {e}")

    def send_command(self, command: str):
        """
        Sends a command string to Arduino.
        Example: send_command("RED")
        Arduino receives: "RED\n"
        """
        if self.ser.is_open:
            message = command.strip() + "\n"
            self.ser.write(message.encode("utf-8"))

    def read_response(self):
        """
        Reads a line back from Arduino (optional).
        Useful for debugging — Arduino sends "OBSTACLE_DETECTED" etc.
        """
        if self.ser.in_waiting > 0:
            response = self.ser.readline().decode("utf-8").strip()
            return response
        return None

    def close(self):
        if self.ser.is_open:
            self.ser.close()
            print("Serial connection closed.")
