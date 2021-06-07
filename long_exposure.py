# -*- coding: utf-8 -*-
"""
Created on Thu May 20 22:43:04 2021

@author: LENOVO
"""

#ovaj kod je za obradu video snimka koji je sniman

import numpy as np
import cv2
from PIL import Image
import os


def sum_arr(arr):
    nframe = int(arr.shape[0])

    res = np.sum(arr,axis=0)//nframe
    print(res.shape)
    return res

def to_array(video_name):
    cap = cv2.VideoCapture(video_name)
    num_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width_of_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_of_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    arr = np.empty((num_of_frames, height_of_frame, width_of_frame, 3), np.dtype('uint8'))

    br = 0
    ret = True

    while (br < num_of_frames  and ret):
        ret, arr[br] = cap.read()
        br += 1
    
    return arr

def get_orange(pic):
    
    hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,(0, 120, 90), (11, 180, 255) )
    
    return mask
def for_all_orange(arr):
    nf = int(arr.shape[0])
    out = get_orange(arr[0])
    for i in range(nf):
        pic2 = get_orange(arr[i])
        out = np.bitwise_or(out,pic2)
    out1 = Image.fromarray(np.uint8(out))
    out1.show()
    newsize = (28,28)
    out1_r = out1.resize(newsize)
    out1_r.show()

    out1_r.save("output_test.png")
    return out
def resize_and_prepare(pic):
    newsize = (28, 28)
    pic_s =pic.resize(newsize)
    pic_s.save("output_test.png")
    
    
    
    
if __name__ == "__main__":
    name_of_video = 'output_br_test.avi'
    arr_4d = to_array(name_of_video)
    pict_= arr_4d[0];
    mask_ = get_orange(pict_)
    outt = for_all_orange(arr_4d)
    print('gotov sam sa long_exsposure kododm')
    #poziva dalje da klasifikator otkrije na osnovu slike koja je cifra ispisana
    os.system('python -W ignore CNN_classificator.py')
   
