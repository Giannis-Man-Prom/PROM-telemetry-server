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

        if op_sys == "Linux" or op_sys == "Windows" or op_sys == "Darwin":
            for port in [port for port in self.ports if port.serial_number == '3086377C3233' or port.serial_number =='58CD180181']:
                # extracting only the string necessary for the connection to the usb and to the lib

                sub_string = self.__substring_extractor(r'^([^ ]+)', str(port)).group(1)

                """Attempts to open the serial connection."""
                while True:
                    try:
                        print("Opening the serial port connection")
                        serial_connection_inst.port = port.device
                        serial_connection_inst.timeout = 1
                        serial_connection_inst.open()

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