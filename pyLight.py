import keyboard
import time
from NeoPixelStrip import Strip

class KeyboardController(object):
    def __init__(self, com):
        self.strip = Strip(com)
        keyboard.hook(self.event_hook)
        self.volume_level = 0

        self.dispatch = dict()
        self.dispatch['esc'] = self.esc_press
        self.dispatch['volume up'] = self.volume_change
        self.dispatch['volume down'] = self.volume_change


    def event_hook(self, event):
        if len(keyboard._pressed_events) > 0:
            try:
                self.dispatch[event.name](event)
            except KeyError:
                pass
        elif 'volume' in event.name:
            pass
        else:
            self.strip.send_uniform_color()
            print("sent off")

        time.sleep(self.strip.MIN_PERIOD)  # Prevent serial buffer overflow

    def esc_press(self, event):
        if event.event_type == 'down':
            self.strip.send_uniform_color(31, 0, 0)

    def volume_change(self, event):
        if event.name == "volume up" and event.event_type == "down":
            self.volume_level += 1
        elif event.name == "volume down" and event.event_type == "down":
            self.volume_level -= 1

        c = [[0, 0, 0] for _ in range(self.strip.LEN)]
        c[:self.volume_level] = [[31, 31, 31] for _ in range(self.volume_level)]
        self.strip.send_colors(c)


controller = KeyboardController('COM4')

keyboard.wait()  # used to keep application alive.
                 # Should be taken care of by UI application in future
