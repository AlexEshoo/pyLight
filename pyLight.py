import serial
import time
import struct

comm = serial.Serial('COM4', 115200, timeout=.1)
inp = [0] * 90

def serializeColor(R,G,B):
	bits = B | (G << 5) | (R << 10)
	
	num = struct.pack('H', bits)
	
	return num

bum = serializeColor(3,2,1)
mub = struct.unpack('H',bum)

print(mub)
print(bin(mub[0]))

while True:
    msg = b''
    if inp[0] == 0:
        inp = [1,85,170]
    else:
        inp = [0] * 3

    for n in range(len(inp)):
        msg += struct.pack('B', inp[n])
    comm.write(msg)
    time.sleep(1)