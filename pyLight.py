import keyboard
import time
from NeoPixelStrip import Strip
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from math import ceil
import init_parmeters


class KeyboardController(object):
    def __init__(self, com):
        self.strip = Strip(com)
        keyboard.hook(self.event_hook)

        self.CONFIG_PARAMS = init_parmeters.CONFIG_PARAMETERS

        # Get initial interface volume level. Windows Only.
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        scalar_volume = self.volume.GetMasterVolumeLevelScalar()
        self.volume_level = self._translate(scalar_volume, 0, 1, 0, self.strip.LEN)

        # Setup dispatcher for callback functions on keypress
        self.dispatch = dict()
        self.dispatch['esc'] = self.esc_press
        self.dispatch['volume up'] = self.volume_change
        self.dispatch['volume down'] = self.volume_change
        for i in range(97, 123):
            self.dispatch[chr(i)] = self.letter_press
        for i in range(10):
            self.dispatch[str(i)] = self.number_press

    def event_hook(self, event):
        try:
            self.dispatch[event.name](event)
        except KeyError:
            self.other_press(event)

        time.sleep(self.strip.MIN_PERIOD)  # Prevent serial buffer overflow

    def esc_press(self, event):
        if event.event_type == 'down':
            self.strip.send_uniform_color(31, 0, 0)
        elif len(keyboard._pressed_events) == 0:
            self.strip.send_uniform_color()

    def letter_press(self, event):
        if event.event_type == 'down':
            self.strip.send_uniform_color(0, 10, 20)
        elif len(keyboard._pressed_events) == 0:
            self.strip.send_uniform_color()

    def number_press(self, event):
        num = int(event.name)
        if event.event_type == 'down':
            self.strip.send_single_color(num, 0, 10, 0)
        else:
            self.strip.send_single_color(num)

    def volume_change(self, event):
        if event.event_type == "down":
            scalar_volume = self.volume.GetMasterVolumeLevelScalar()
            self.volume_level = self._translate(scalar_volume, 0, 1, 0, self.strip.LEN)

            c = [[0, 0, 0] for _ in range(self.strip.LEN)]
            c[:self.volume_level] = [self.CONFIG_PARAMS['VolumeColor'] for _ in range(self.volume_level)]
            self.strip.send_colors(c)

    def other_press(self, event):
        pass

    def _rainbow(self):
        """
        This is approximation. Will not cycle all
        colors obviously. performance is not
        great, but its a proof of concept.
        :return:
        """
        while True:
            for i in range(32):
                rgb = self._wheel(i)
                self.strip.send_uniform_color(rgb[0], rgb[1], rgb[2])
                time.sleep(0.1)

    def _wheel(self, wheel_pos):
        wheel_pos = 31 - wheel_pos
        if wheel_pos < 11:
            return [ 31 - wheel_pos * 3, 0, wheel_pos * 3 ]
        if wheel_pos < 21:
            wheel_pos -= 10
            return [ 0, wheel_pos * 3, 31 - wheel_pos * 3 ]
        wheel_pos -= 21
        return [ wheel_pos * 3, 31 - wheel_pos * 3, 0 ]

    @staticmethod
    def _translate(value, left_min, left_max, right_min, right_max):
        left_span = left_max - left_min
        right_span = right_max - right_min
        value_scaled = float(value - left_min) / float(left_span)
        return int(ceil(right_min + (value_scaled * right_span)))


controller = KeyboardController('COM4')

keyboard.wait()  # used to keep application alive.
# Should be taken care of by UI application in future
