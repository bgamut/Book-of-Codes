"""
opencv wheel has been downloaded from
https://www.lfd.uci.edu/~gohlke/pythonlibs/
pip has been updated before pip installing the wheel
"""
import cv2
import numpy as numpy
from sentiment import *
def display_image(file):
    relative_file = relativepath(file)
    img=cv2.imread(relative_file)
    cv2.imshow('image',img)
    k=cv2.waitKey(0)
    if k== 27:
        cv2.destryAllWindows()
    elif k== ord('s'):
        cv2.imwrite('messigray.png',img)
        cv2.destroyAllWindows()
        
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

# Release everything if job is finished
