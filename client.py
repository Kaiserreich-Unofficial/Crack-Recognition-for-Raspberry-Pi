from PIL import Image
import socket
from os import system
from easygui import msgbox
from unet import Unet
import requests
import re
from io import BytesIO

#初始化神经网络
unet = Unet()
#打开监控主页
system('index.html')


def load_map(N,E):
    url = 'https://restapi.amap.com/v3/staticmap?location='+E+','+N+'&zoom=17&size=1024*1024&markers=mid,,A:'+E+','+N+'&key=58418ef35fcd06ab4e2378822f92baa2'
    response=requests.get(url)
    data=response.content
    img = Image.open(BytesIO(data))
    img.save('location.png')

#接口定义
try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect(('192.168.137.21', 9600))
    tcp_socket.send("start".encode('utf8'))
except:
    msgbox('服务器未连接，请检查设备是否开机！','Warning','我知道了')
    exit(0)

while True:
    string = tcp_socket.recv(16)
    try:
        allLen = int(string.decode())
        if allLen <= 100000:
            print(allLen)
            curSize = 0
            allData = b''
            while curSize < allLen - 1024:
                data = tcp_socket.recv(1024)
                allData += data
                curSize += len(data)
            data = tcp_socket.recv(allLen - curSize)
            allData += data
            image = Image.open(BytesIO(allData))
            image.save('origin.jpg')
            r_image = unet.detect_image(image)
            r_image.save('crack.jpg')


            string = tcp_socket.recv(30)
            string = re.match('(\d+.\d+)N(\d+.\d+)E',string.decode())
            if string:
                print(string.group(1)+'N',string.group(2)+'E')
                load_map(string.group(1), string.group(2))
                
    except:
        pass