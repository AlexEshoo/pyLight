import serial
import time
import struct


class Strip(object):
    def __init__(self, com):
        self.COM = self.connect_arduino(com)
        self.OFF = self._serialize_color(0, 0, 0, False)
        self.LEN = 30  # Length of strip.
        self.MIN_PERIOD = 0.008 # minimum period of cycling

        # .. todo:: Enable use of different length strips.

    @staticmethod
    def connect_arduino(com):
        # Arduino Board Resets every time the serial communication is activated and deactivated.
        # This means that when this script starts there will be a delay before the arduino starts
        # responding. Keeping DTR High or Low seems to have no effect.
        comm = serial.Serial(com, 115200, timeout=0.1)
        time.sleep(2)  # Allow Arduino reset to happen to prevent buffer offset

        return comm

    @staticmethod
    def _serialize_color(r, g, b, x=False):
        """
        Packs color values into two serial bytes to be read by the arduino.
        
        :param r: Red Value int from 0 to 31
        :param g: Green Value int from 0 to 31
        :param b: Blue Value int from 0 to 31
        :param x: Extra bit. Unused for now. (bool)
        :returns: Packed bytes object of length 2
        """
        try:
            r = int(r)
            g = int(g)
            b = int(b)
        except ValueError:
            print("Color values must be numeric")
            return None

        for c in [r, g, b]:
            if c not in range(32):
                print("Color values must be between 0 and 31")  # Make exceptions?
                return None

        bits = b | (g << 5) | (r << 10) | (x << 15)  # Bitshift values together

        num = struct.pack('H', bits)  # Encode as unsigned long

        return num

    def _send_color(self, r=0, g=0, b=0, x=False):
        ser_color = self._serialize_color(r, g, b, x)
        self.COM.write(ser_color)
        return None

    def send_colors(self, led_list):
        if len(led_list) < self.LEN:
            diff = self.LEN - len(led_list)
            led_list.extend([[0,0,0]]*diff)

        for k in range(self.LEN):
            r = led_list[k][0]
            g = led_list[k][1]
            b = led_list[k][2]
            self._send_color(r,g,b)

    def send_single_color(self, led, r, g, b):
        for k in range(self.LEN):
            if k == led:
                self._send_color(r,g,b)
            else:
                self._send_color()

    def send_uniform_color(self, r=0, g=0, b=0):
        for k in range(self.LEN):
            self._send_color(r, g, b)
        return None
