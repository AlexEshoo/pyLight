import serial
import time
import struct

# Arduino Board Resets everytime the serial communication is activated and deactivated.
# This means that when this script starts there will be a delay before the arduino starts
# responding. Keeping DTR High or Low seems to have no effect.

comm = serial.Serial('COM4', 115200, timeout=.1)

inp = [0] * 90

def serializeColor(R,G,B):
	bits = B | (G << 5) | (R << 10)
	
	num = struct.pack('H', bits)
	
	return num

bum = serializeColor(0,0,0)
print(bin(struct.unpack('H',bum)[0]))

i=0
while True:
	comm.write(serializeColor(0,i,0))
	result = comm.read()
	if result != b'':
		print('byte1:', struct.unpack('B',result))
	result = comm.read()
	if result != b'':
		print('byte2:', struct.unpack('B',result))
	
	if i < 31: i += 1
	else: i = 0
	time.sleep(1)
	

#time.sleep(1)
#comm.write(struct.pack('B', 10))

while False:
    msg = b''
    if inp[0] == 0:
        inp = [1,85,170]
    else:
        inp = [0] * 3

    for n in range(len(inp)):
        msg += struct.pack('B', inp[n])
    comm.write(msg)
    time.sleep(1)