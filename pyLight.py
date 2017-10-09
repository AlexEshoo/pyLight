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
        if len(keyboard._pressed_events) > 0:
            try:
                self.dispatch[event.name](event)
            except KeyError:
                pass

        elif 'volume' in event.name:
            pass  # Needed to prevent immediate off command for volume indication

        else:
            self.strip.send_uniform_color()

        time.sleep(self.strip.MIN_PERIOD)  # Prevent serial buffer overflow

    def esc_press(self, event):
        if event.event_type == 'down':
            self.strip.send_uniform_color(31, 0, 0)

    def letter_press(self, event):
        if event.event_type == 'down':
            self.strip.send_uniform_color(0, 10, 20)

    def number_press(self, event):
        if event.event_type == 'down':
            num = int(event.name)
            self.strip.send_single_color(num, 0, 10, 0)

    def volume_change(self, event):
        if event.event_type == "down":
            scalar_volume = self.volume.GetMasterVolumeLevelScalar()
            self.volume_level = self._translate(scalar_volume, 0, 1, 0, self.strip.LEN)

            c = [[0,0,0] for _ in range(self.strip.LEN)]
            c[:self.volume_level] = [self.CONFIG_PARAMS['VolumeColor'] for _ in range(self.volume_level)]
            self.strip.send_colors(c)

    def _translate(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return int(ceil(rightMin + (valueScaled * rightSpan)))


controller = KeyboardController('COM4')

keyboard.wait()  # used to keep application alive.
                 # Should be taken care of by UI application in future
