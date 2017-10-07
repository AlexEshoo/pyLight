import serial
import time
import struct

# Arduino Board Resets everytime the serial communication is activated and deactivated.
# This means that when this script starts there will be a delay before the arduino starts
# responding. Keeping DTR High or Low seems to have no effect.

comm = serial.Serial('COM4', 115200, timeout=.1)
time.sleep(2) # WAIT FOR RESET TO OCCUR ON SERIAL CONNECT
def serializeColor(R,G,B):
	bits = B | (G << 5) | (R << 10)
	
	num = struct.pack('H', bits)
	
	return num

i=0
while True:
	c = serializeColor(i,i,i)
	off = serializeColor(0,0,0)
	for k in range(30):
		if k % 2 == 0:
			comm.write(c)
		else:
			comm.write(off)
	if i < 30: i += 1
	else: i = 0
	time.sleep(0.008) # Fastest you can go without overflow ~= 0.008
