import socket
import cv2
import threading
import struct
import numpy
import pyautogui

class Mouse_Connect_Object:
    def __init__(self, D_addr_port=["", 8880]):
        self.position = [0,0]
        self.addr_port = D_addr_port
        self.src = 888+ 60  # 双方确定传输帧数，（888）为校验值
        self.interval = 0  # 图片播放时间间隔
        self.img_fps = 60  # 每秒传输多少帧数

    def Set_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def Socket_Connect(self):
        self.Set_socket()
        self.client.connect(self.addr_port)
        print("IP is %s:%d" % (self.addr_port[0], self.addr_port[1]))

    def RT_Image(self):
        # 按照格式打包发送帧数和分辨率
        self.name = self.addr_port[0] + " Camera"
        self.position[0],self.position[1] = pyautogui.size()
        print(self.position[0],self.position[1])
        self.client.send(struct.pack("ll",self.position[0],self.position[1]))
        while(1):


            Position =struct.unpack("ll", self.client.recv(8))
            print(Position)
            print(Position[0], Position[1])
            try:
                pyautogui.moveTo(Position[0], Position[1])
            except:
                pass;
            finally:
                if (pyautogui.keyDown == 27):  # 每10ms刷新一次图片，按‘ESC’（27）退出
                    self.client.close()
                    cv2.destroyAllWindows()
                    break

    def Get_Data(self, interval):
        showThread = threading.Thread(target=self.RT_Image)
        showThread.start()


if __name__ == '__main__':
    mouse = Mouse_Connect_Object()
    mouse.addr_port[0] = input("Please input IP:")
    mouse.addr_port = tuple(mouse.addr_port)
    mouse.Socket_Connect()
    mouse.Get_Data(mouse.interval)
