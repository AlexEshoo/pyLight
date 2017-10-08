import keyboard
import time
from NeoPixelStrip import Strip

class KeyboardController(object):
    def __init__(self, com):
        self.strip = Strip(com)
        keyboard.hook(self.event_hook)
        self.volume_level = 0

    def event_hook(self, event):
        print(event.name)
        if event.name == "volume up" and event.event_type == "up":
            self.volume_level += 1
            for k in range(self.strip.LEN):
                if self.volume_level > k:
                    self.strip._send_color(31,31,31)
                else:
                    self.strip._send_color(0,0,0)
        elif event.name == "volume down" and event.event_type == "down":
            self.volume_level -= 1
            for k in range(self.strip.LEN):
                if self.volume_level > k:
                    self.strip._send_color(31,31,31)
                else:
                    self.strip._send_color(0,0,0)
        elif 'volume' in event.name:
            pass
        elif len(keyboard._pressed_events) > 0:
            self.strip.send_uniform_color(10,0,0)
        else:
            self.strip.send_uniform_color()

        time.sleep(0.008)  # Prevent serial buffer overflow

controller = KeyboardController('COM4')

keyboard.wait()  # used to keep application alive.
                 # Should be taken care of by UI application in future

