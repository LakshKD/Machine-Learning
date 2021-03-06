# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/laksh/.spyder2/.temp.py

"""
import cv2
import numpy as np

def img_binarizer(image,median_list):
    height, width = image.shape[:2]
    image_list = []
    for p in range(9):
        a = median_list[p]
       
        
        data = np.zeros([height, width])
        for i in range(height):
            for j in range(width):
                if image.item(i,j,2) >= a[0] and image.item(i,j,1) >= a[1] and image.item(i,j,0) >= a[2] :
                    data[i,j]=0
                else:
                    data[i,j]=255
               
        image_list.append(data)       
    return image_list       