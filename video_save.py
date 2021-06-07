# -*- coding: utf-8 -*-
"""
Created on Thu May 20 22:43:42 2021

@author: LENOVO
"""

import numpy as np
import cv2
import os


cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_br_test.avi',fourcc, 0.010, (640,480))


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,1)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

#ovo brisi ako ne valja
os.system('python -W ignore long_exposure.py')