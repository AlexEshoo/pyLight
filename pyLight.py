import serial
import time
import struct

# Arduino Board Resets everytime the serial communication is activated and deactivated.
# This means that when this script starts there will be a delay before the arduino starts
# responding. Keeping DTR High or Low seems to have no effect.

comm = serial.Serial('COM4', 115200, timeout=.1)

def serializeColor(R,G,B):
	bits = B | (G << 5) | (R << 10)
	
	num = struct.pack('H', bits)
	
	return num

i=0
while True:
	comm.write(serializeColor(i,i,i))
	if i < 31: i += 1
	else: i = 0
	time.sleep(0.05)
