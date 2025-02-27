import json
import logging
import time

import serial.tools.list_ports
import platform
from enum import Enum
import os
import re
from dotenv import load_dotenv

from custom_exceptions.serial_connection_exception import SerialConnectionException


class Season(Enum):
    Linux = "Linux"
    Win = "Windows"
    Mac = "Darwin"


class SerialRead:
    # Connect the path with your '.env' file name
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

    __serial_baudrate = os.getenv('SERIAL_BAUDRATE')
    __serial_bytesize = os.getenv('BYTESIZE')

    def __init__(self):

        self.ports = serial.tools.list_ports.comports()
        self.serialInst = self.establish_connection_based_on_op_sys()

    def __substring_extractor(self, regex, string):
        # extracting only the string necessary for the connection to the usb and to the lib
        return re.match(regex, string)

    def close_serial_connection(self):
        self.serialInst.close()

    def establish_connection_based_on_op_sys(self):
        op_sys = platform.system()
        # The module gives us the option to first create the object and then define the variables needed for the connection
        serial_connection_inst = serial.Serial(timeout=0.4)

        serial_connection_inst.baudrate = int(self.__serial_baudrate)
        serial_connection_inst.bytesize = int(self.__serial_bytesize)

        seth = re.compile(r'.*(usbserial|usbmodem|serial|stm|STM|STM32|Σειριακή συσκευή ).*')

        if op_sys == "Linux":

            return "this is a Linux"



        elif op_sys == "Windows":

            for port in [port for port in self.ports if seth.search(str(port))]:
                # extracting only the string necessary for the connection to the usb and to the lib

                sub_string = self.__substring_extractor(r'^([^ ]+)', str(port)).group(1)

                """Attempts to open the serial connection."""
                while True:
                    try:
                        print("Opening the serial port connection")
                        serial_connection_inst.port = sub_string
                        serial_connection_inst.timeout = 0.5
                        serial_connection_inst.open()

                        break

                    except serial.SerialException as e:
                        print(f"Error opening serial port: {e}")
                        time.sleep(0.6)

            if serial_connection_inst.is_open:
                return serial_connection_inst

            else:
                return None

        elif op_sys == "Darwin":  # Mac

            for port in [port for port in self.ports if seth.search(str(port))]:
                #extracting only the string necessary for the connection to the usb and to the lib
                sub_string = self.__substring_extractor(r'^([^ ]+)', str(port)).group(1)

                """Attempts to open the serial connection."""
                while True:
                    try:
                        print("Opening the serial port connection")
                        serial_connection_inst.port = sub_string
                        serial_connection_inst.timeout = 0.5
                        serial_connection_inst.open()
                        print("Serial connection Oppened")
                        break

                    except serial.SerialException as e:
                        print(f"Error opening serial port: {e}")
                        time.sleep(0.6)

            if serial_connection_inst.is_open:
                return serial_connection_inst
            else:
                return None

        else:
            return None  # If platform does not match any of the operating systems from above we will not try something

    def read_from_serial(self):

        if self.serialInst is None:
            raise SerialConnectionException("The serial connection did not open")

        try:
            if self.serialInst.in_waiting > 0:
                # Read a line from the serial buffer
                line = self.serialInst.read_until(b'\n').decode('utf-8').strip()

                # Print the JSON data
                return line

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":

    telemetry = SerialRead()

    while 1:
        # print(telemetry.serialInst.in_waiting)

        print(telemetry.serialInst.read_until(b'\n').decode('utf-8').strip())

        time.sleep(0.1)
    # with open('serial_data.txt', 'w') as file:

        # while 1:
        #
        #     print(telemetry.read_from_serial())
        #
        #
        #     if telemetry.read_from_serial() is not None:
        #         # Write data to text file
        #         file.write(telemetry.read_from_serial() + '\n')