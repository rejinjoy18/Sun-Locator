
# coding: utf-8

# In[41]:

import numpy as np
import imutils
import cv2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("path", help = "path to image file")
args = parser.parse_args()
path = args.path


center = None
LowerBound = (20, 100, 100)
UpperBound = (30, 255, 255) # credit: aishack.in for hsv range of values for yellow color

img = cv2.imread(path)
blur = cv2.GaussianBlur(img, (5, 5), 0)

## converting to hsv mode
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, LowerBound, UpperBound)

area = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  ### credit to opencvexamples.blogspot.com

if len(area) > 0:

    ## finding largest contour in area
    large = max(area, key=cv2.contourArea)
    
    ### finding minimum enclosing circle of contour found
    ((x, y), r) = cv2.minEnclosingCircle(large)
    
    ## finding centroid of contour
    M = cv2.moments(large)
    
    ## formula of centroid obtained from : 
    ## http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


    cv2.circle(img, (int(x), int(y)), int(r), (0, 0, 0), 2)

cv2.imwrite('sun_' + path, img)

