import serial
import time
import struct

comm = serial.Serial('COM4', 115200, timeout=.1)
inp = [0] * 90

while True:
    msg = b''
    if inp[0] == 0:
        inp = [10] * 3
    else:
        inp = [0] * 3

    for n in range(len(inp)):
        msg += struct.pack('B', inp[n])
    comm.write(msg)
    time.sleep(1)
