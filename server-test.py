import socket
import os
import cv2 as cv
import serial
import re
from PIL import Image
from io import BytesIO

# 读取设施
cap = cv.VideoCapture('/dev/video0', cv.CAP_V4L)
# 读取摄像头FPS
fps = cap.get(cv.CAP_PROP_FPS)
#初始化GPS模块
ser = serial.Serial("/dev/ttyS0",115200) #115200是GT-U13的波特率

# set dimensions 设置分辨率
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1024)

def PIL2bytes(im):
    bytesIO = BytesIO()
    im.save(bytesIO, format='JPEG')
    return bytesIO.getvalue()

#初始化TCP接口
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
tcp_socket.bind(('192.168.137.223', 9600))
tcp_socket.listen(128)
client, addr = tcp_socket.accept()

data = client.recv(1024)

if data.decode('utf8') == 'start':
    while True:
        ret, frame = cap.read()
        if ret:
            frame = frame[:,:,::-1]
            img = Image.fromarray(frame)
            img = img.rotate(180)
            picBytes = PIL2bytes(img)
            picSize = len(picBytes)
            client.send(str(picSize).encode())
            client.sendall(picBytes)
            line = 'b\'$GNRMC,130416.000,A,2234.74883,N,11356.77128,E,1,20,1.21,47.2,M,-2.5,M,,*54\''
            m = re.match(r'b\'\$GNRMC,(\d+.\d+),(\d+).(\d+),N,(\d+).(\d+),E',line)
            if m:
                location = m.group(2)[:-2]+'.'+m.group(2)[-2:]+m.group(3)[:-2]+'N'+m.group(4)[:-2]+'.'+m.group(4)[-2:]+m.group(5)[:-2]+'E'
                while len(location.encode()) < 30:
                    location += ' '
                client.send(location.encode())
            else:
                client.send('No GPS signal!'.encode())