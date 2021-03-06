#!/usr/bin/env python

'''
face detection using haar cascades

USAGE:
    facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

# Python 2/3 compatibility
from __future__ import print_function

import subprocess
import time
import os
import signal
import numpy as np
import cv2
import math as m
import findmediannew as f

# local modules
from video import create_capture
from common import clock, draw_str
flag = 1


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=3, minNeighbors=10, minSize=(50, 50),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    if(len(rects) > 1) :
        return (img, 0)
    for x1, y1, x2, y2 in rects:
        h = abs(y2-y1)
        w = abs(x2-x1)
        if(w > 150 or h > 150):
            break
        crop_img = img[y1:(y1+h), x1:(x1+w)]
        mimg, cnt = f.preprocessImage(crop_img)
        img[y1+3:(y1+h)-(h/5), x1+3:(x1+w)-6] = mimg
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        return (img, cnt)

if __name__ == '__main__':
    import sys, getopt
    print(__doc__)

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try:
        video_src = video_src[0]
    except:
        video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "../../data/haarcascades/cascade.xml")
    #nested_fn  = args.get('--nested-cascade', "../../data/haarcascades/haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)
    #nested = cv2.CascadeClassifier(nested_fn)

    cam = create_capture(video_src, fallback='synth:bg=../data/lena.jpg:noise=0.05')
    average = False
    avgImg = []
    while True:
        if(average == False) :
            average = True
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        t = clock()
        rects = detect(gray, cascade)
        vis = img.copy()
        ret = draw_rects(vis, rects, (0, 255, 0))
        if(ret != None) :
        	(vis, cnt) = ret
        cnt = cnt+1
        if(cnt == 5 and flag == 1):
            flag=0
            subprocess.call(['./music.sh'], shell=True)
        if(cnt == 2):
            flag = 1
            subprocess.call(['./kill.sh'], shell=True)
        draw_str(vis, (20, 20), 'finger count: %d' % cnt)
        cv2.imshow('facedetect', vis)
        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()
