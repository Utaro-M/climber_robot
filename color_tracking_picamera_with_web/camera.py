#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import sys

def show():

    #from web
    URL = "http://192.168.128.101:8000/stream.mjpg"
    s_video = cv2.VideoCapture(URL)
    while(True):
        #from web
        ret, frame = s_video.read()
        cv2.imshow("Stream Video",frame)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break


if __name__ == "__main__":
    try:
        print("OK")
        show()
    except:
        print("exit")
        sys.exit()
