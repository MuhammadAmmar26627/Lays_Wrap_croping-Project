import cv2
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize']=(10,10)
import pandas as pd
from numpy.core.fromnumeric import shape
kernal=np.ones((2,2))
def dis(x1,x2,y1,y2):
    return sqrt(((x1-x2)**2)+((y1-y2)**2))
def empty(*arg):
    pass
def getcountour(img,imgContour):
    global a
    countours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#     cv2.drawContours(imgContour,countours,-1,(255,0,255),5)
#     a=countours
    for cnt in countours:
        if len(cnt)>0:
            area=cv2.contourArea(cnt)
            if area>10:
                a.append(cnt)
                print('a')
                cv2.drawContours(imgContour,cnt,-1,(255,0,255),1)
cv2.namedWindow('th')
cv2.resizeWindow('th',(600,85))
cv2.createTrackbar('thr1','th',90,255,empty)
cv2.createTrackbar('thr2','th',90,255,empty)
while True:
    img=cv2.imread('1.jpg')
    
    print(np.shape(img))
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask_image=cv2.inRange(hsv,np.array((0,0,0)),np.array((180,255,40)))
    contour,hierarchy=cv2.findContours(mask_image,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    contour=sorted(contour,key=lambda x:cv2.contourArea(x),reverse=True)
    for cnt in contour:

        area=cv2.contourArea(cnt)
#     if area>30000:
        if (area>40000) & (area<1400000):
#         print(area)
#         a.append(cnt)
            cv2.drawContours(img, cnt, -1, (0, 255, 0), 10)
    # plt.imshow(img[:,:,::-1])
    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break