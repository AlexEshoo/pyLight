import serial
import time
import struct

def connectArduino(COM):
    # Arduino Board Resets everytime the serial communication is activated and deactivated.
    # This means that when this script starts there will be a delay before the arduino starts
    #responding. Keeping DTR High or Low seems to have no effect.
    comm = serial.Serial(COM, 115200, timeout=0.1)
    time.sleep(2) # Allow Ardunio reset to happen to prevent buffer offset
    
    return comm

def serializeColor(R,G,B,X=False):
    """
    Packs color values into two serial bytes to be read by the arduino.
    
    :param R: Red Value int from 0 to 31
    :param G: Green Value int from 0 to 31
    :param B: Blue Value int from 0 to 31
    :param X: Extra bit. Unused for now. (bool)
    :returns: Packed bytes object of length 2
    """
    try:
        R = int(R)
        G = int(G)
        B = int(B)
    except ValueError:
        print("Color values must be numeric")
        return None

    for c in [R, G, B]:
        if not c in range(32):
            print("Color values must be between 0 and 31") # Make exceptions?
            return None

    bits = B | (G << 5) | (R << 10) | (X <<15) # Bitshift values together
    
    num = struct.pack('H', bits) # Encode as unsigned long
    
    return num

def sendColor(com, serColor):
    com.write(serColor)
    
def test():
    i=0
    while True:
        c = serializeColor(i,i,i)
        OFF = serializeColor(0,0,0)
        for k in range(30):
            if k % 2 == 0:
                sendColor(comm, c)
            else:
                sendColor(comm, OFF)
        if i < 30: i += 1
        else: i = 0
        time.sleep(0.008) # Fastest you can go without overflow ~= 0.008 (125Hz)

comm = connectArduino('COM4')
