import keyboard
import time
from NeoPixelStrip import Strip

class KeyboardController(object):
    def __init__(self, com):
        self.strip = Strip(com)
        keyboard.hook(self.event_hook)

    def event_hook(self, event):
        event.name
        if len(keyboard._pressed_events) > 0:
            self.strip.send_uniform_color(10,0,0)
        else:
            self.strip.send_uniform_color()

        time.sleep(0.008)  # Prevent serial buffer overflow

controller = KeyboardController('COM4')

keyboard.wait()  # used to keep application alive.
                 # Should be taken care of by UI application in future

