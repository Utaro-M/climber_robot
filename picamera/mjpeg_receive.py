#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import sys

URL = "http://192.168.128.101:8000/stream.mjpg"
s_video = cv2.VideoCapture(URL)

try:

    while True:
      ret, img = s_video.read()
      cv2.imshow("Stream Video",img)
      key = cv2.waitKey(1) & 0xff
      if key == ord('q'): break
except:
    sys.exit()
