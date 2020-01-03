#-*- coding:utf-8 -*-

from websocket import create_connection
import sys
import base64
from io import BytesIO
import cv2
import numpy as np

ws = create_connection("ws://192.168.128.101:8080/camera")
print("connected")

# decode
while True:
    print(ws.recv())
    arr = np.asarray(bytearray(ws.recv()), dtype=np.uint8)
    print("in2")
    img = cv2.imdecode(arr, -1)  # 'load it as it is'
    print("in3")
    cv2.imshow('image', img)
    cv2.waitKey(10)
    print("in")
cv2.destroyAllWindows()

ws.close()
