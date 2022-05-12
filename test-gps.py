import serial
import time
ser = serial.Serial("/dev/ttyS0",115200) #115200是GT-U13的波特率
while True:
    line = str(ser.readline())
    if line:
        print(line)