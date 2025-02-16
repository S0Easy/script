# -*- coding: utf-8 -*-
import numpy as np  
import cv2  
import pyautogui  
import time  
  
# 设置屏幕分辨率和帧率  
screen_size = (3440,1440)  
fps = 30.0  
  
# 初始化 VideoWriter 对象  
fourcc = cv2.VideoWriter_fourcc(*'XVID')  
out = cv2.VideoWriter('output.avi', fourcc, fps, screen_size)  
  
# 录屏时间（秒）  
# record_time = 30 
  
# 开始录屏  
start_time = time.time()  
print('START...')  
# while (time.time() - start_time) < record_time:  
while True:
    # 截取屏幕  
    screenshot = pyautogui.screenshot()  
    # 将截图转换为numpy数组  
    frame = np.array(screenshot)  
    # OpenCV默认为BGR颜色空间，而PIL图像为RGB，需要转换颜色通道  
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
    # 写入帧  
    out.write(frame)  
    # 等待一段时间以达到期望的帧率  
    time.sleep(1/fps)  
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
  
# 释放 VideoWriter 对象  
out.release()
print('END！')  
