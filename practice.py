import cv2
import numpy as np

cap=cv2.VideoCapture(0)

while(True):
    ret,frame=cap.read()
    print(frame)
    #cv2.imshow('frame1',frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
