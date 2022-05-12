# Crack-Recognition-for-Raspberry-Pi
这是一个为树莓派编写的裂缝识别程序，语义分解部分基于bubbliiiing的Resnet50网络，带有一个监控前端
## 源码地址
https://github.com/bubbliiiing/unet-pytorch
## 系统环境
### Raspberry Pi 4B(Server):
GT-U13 GPS 模块

Raspi-OS(bullseye)

numpy

opencv-python

pillow

pyserial

### PC(client):
easygui

pillow

## 使用方法
将server.py和server-test.py拷贝至树莓派的~(/home/pi)目录下，并修改server和server-test的tcp_scoket的ip为树莓派本机ip

server.py是带有GPS模块的服务端脚本(若你的设备没有GPS请运行server-test.py)

将client.py中的tcp_scoket的ip也修改为树莓派的ip

将unet.py中的model_path调整为你的训练权重(放在logs文件夹里),并配置你的num_classes,input_shape和mix_type

在树莓派上运行server.py(如无GPS情况下,请运行server-test.py,模拟定位在广州)

在PC上运行client.py,程序会自动在浏览器中打开监控前端

## 注意事项

如果不想适用CUDA加速,或者电脑没有安装NVDIA独立显卡,请在unet.py中将CUDA设置为False

低技术力屑作,如有问题请在ISSUE中指出
