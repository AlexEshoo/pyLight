import serial
import time
import struct

from math import ceil


class Strip(object):
    def __init__(self, com, mode=0):
        self.MODE = mode
        self.COM = self.connect_arduino(com, self.MODE)
        self.OFF = self._serialize_color(0, 0, 0, False)
        self.LEN = 30  # Length of strip.
        self.MIN_PERIOD = 0.008  # minimum period of cycling

        # .. todo:: Enable use of different length strips.

    def connect_arduino(self, com, mode=0):
        # Arduino Board Resets every time the serial communication is activated and deactivated.
        # This means that when this script starts there will be a delay before the arduino starts
        # responding. Keeping DTR High or Low seems to have no effect.
        comm = serial.Serial(com, 115200, timeout=0.1)
        time.sleep(2)  # Allow Arduino reset to happen to prevent buffer offset
        mode_val = struct.pack('B', mode)
        comm.write(mode_val) # Set the serial data processing mode
        time.sleep(2)

        return comm

    def disconnect(self):
        self.COM.close()

    def _serialize_color(self, r, g, b, update=True):
        """
        Packs color values into two serial bytes to be read by the arduino.
        
        :param r: Red Value int from 0 to 255
        :param g: Green Value int from 0 to 255
        :param b: Blue Value int from 0 to 255
        :param update: boolean value. Use to suppress an update.
        :returns: Packed bytes object of length 2
        """
        if self.MODE == 0:
            r = int(ceil(r / 8.3))  # Scale Values to fit in 2/3 of a byte.
            g = int(ceil(g / 8.3))  # Yes, I know how crazy that sounds.
            b = int(ceil(b / 8.3))

            bits = b | (g << 5) | (r << 10) | (update << 15)  # Bitshift values together

            num = struct.pack('H', bits)  # Encode as unsigned long

            return num

    def _send_color(self, r=0, g=0, b=0, update=True):
        if self.MODE == 0:
            ser_color = self._serialize_color(r, g, b, update)
            self.COM.write(ser_color)

        elif self.MODE == 1:
            r_char = struct.pack('B', r)
            g_char = struct.pack('B', g)
            b_char = struct.pack('B', b)
            self.COM.write(r_char)
            self.COM.write(g_char)
            self.COM.write(b_char)

        return None

    def send_colors(self, led_list):
        if len(led_list) < self.LEN:
            diff = self.LEN - len(led_list)
            led_list.extend([[0, 0, 0]] * diff)

        for k in range(self.LEN):
            r = led_list[k][0]
            g = led_list[k][1]
            b = led_list[k][2]
            self._send_color(r, g, b)

    def send_single_color(self, led, r=0, g=0, b=0, clobber=False):
        for k in range(self.LEN):
            if k == led:
                self._send_color(r, g, b)
            elif clobber:
                self._send_color()
            else:
                self._send_color(update=False)

    def send_uniform_color(self, r=0, g=0, b=0):
        if self.MODE == 0:
            for k in range(self.LEN):
                self._send_color(r, g, b)
            return None
        elif self.MODE == 1:
            self._send_color(r, g, b)
