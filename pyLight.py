import keyboard
import time
from NeoPixelStrip import Strip


strip = Strip('COM4')

def event_hook(event):
    if len(keyboard._pressed_events) > 0:
        strip.send_uniform_color(1,1,1)
    else:
        strip.send_uniform_color()

    time.sleep(0.008)  # Prevent serial buffer overflow


keyboard.hook(event_hook)
keyboard.wait()


