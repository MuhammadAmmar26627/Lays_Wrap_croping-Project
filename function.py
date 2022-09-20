import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy.core.fromnumeric import shape

def differnece(img):
    global picture
    img=imutils.rotate_bound(img,-90)
    picture=img.copy()
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    global y
    global y1    
    b=10
    for i in range (17,35):
        mask_image=cv2.inRange(hsv[:,:int(shape(hsv)[1]/3)],np.array((0,0,0)),np.array((180,255,i)))
        plt.imshow(mask_image,cmap='gray')
        contour,hierarchy=cv2.findContours(mask_image,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        contour=sorted(contour,key=lambda x:cv2.contourArea(x),reverse=True)
#         print(i)
        a=[]
        for cnt in contour:
            area=cv2.contourArea(cnt)
            if (area>22000) & (area<26000):
#                 print(area)
                a.append(cnt)
    #             cv2.drawContours(img, cnt, -1, (0, 255, 0), 10)
                (x,y,w,h)=cv2.boundingRect(cnt)
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#                 print(len(a))
                if len(a)==2:
                    b=1
                    break
        if b==1:
            break
            
    x,y,w,h = cv2.boundingRect(a[0])
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    # plt.imshow(img1[:,:,::-1])
    x1,y1,w1,h1 = cv2.boundingRect(a[1])
    cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
#     plt.imshow(img[:,:,::-1])
#     print(cv2.contourArea(a[0]),cv2.contourArea(a[1]))
    
    height=int(x)-int(x1)
    base=int(y)-int(y1)
    # print(height,base)
    from math import atan,degrees
    # try:
    # theta=atan(base/height)
    theta=atan(height/base)
    theta= degrees(theta)
    # except:
    #     theta=0
    theta
    img=picture.copy()
    rot=imutils.rotate(img,angle=-theta)
    plt.imshow(rot[:,:,::-1])

    hsv=cv2.cvtColor(rot,cv2.COLOR_BGR2HSV)
    
    mask_image=cv2.inRange(hsv,np.array((125,100,30)),np.array((255,255,255)))

    contour,hierarchy=cv2.findContours(mask_image,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    contour=sorted(contour,key=lambda x:cv2.contourArea(x),reverse=True)
    
    img=picture.copy()
    img1=imutils.rotate(img,angle=-theta)

    
    a=[]
# print(len(contour))
    for cnt in contour[1:2]:
    #     print(len(cnt))
    #     print(cv2.boundingRect(contour[0]))
    #     (x,y,w,h)=cv2.boundingRect(cnt)
    #     cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        area=cv2.contourArea(cnt)
    #     if area>30000:
        if area>4:
    #         print(area)
            a.append(cnt)
            cv2.drawContours(rot, cnt, -1, (0, 255, 0), 10)
    plt.imshow(rot[:,:,::-1])
    
    x,y,w,h = cv2.boundingRect(a[0])
    cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
    plt.imshow(img1[:,:,::-1])
    
    img1=img1[y:y+h,x:x+w].copy()
    picture=img1.copy()
    
    hsv=cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
#     plt.imshow(hsv)
    
    b=10
    for i in range (17,35):
        mask_image=cv2.inRange(hsv[:,:int(shape(hsv)[1]/3)],np.array((0,0,0)),np.array((180,255,i)))
        plt.imshow(mask_image,cmap='gray')
        contour,hierarchy=cv2.findContours(mask_image,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        contour=sorted(contour,key=lambda x:cv2.contourArea(x),reverse=True)
#         print(i)
        a=[]
        for cnt in contour:
            area=cv2.contourArea(cnt)
            if (area>22000) & (area<26000):
#                 print(area)
                a.append(cnt)
    #             cv2.drawContours(img, cnt, -1, (0, 255, 0), 10)
                (x,y,w,h)=cv2.boundingRect(cnt)
                cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
                print(len(a))
                if len(a)==2:
                    b=1
#                     return img1
                    break
        if b==1:
            break
    # cv2.imshow('1',img1)
    x,y,w,h = cv2.boundingRect(a[0])
    cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
    # plt.imshow(img1[:,:,::-1])
    x1,y1,w1,h1 = cv2.boundingRect(a[1])
    cv2.rectangle(img1,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
    
    print(y,y1)
#     print('asdas')
    # cv2.imshow('2',img1)
    try:
        picture=img1[y1:y,:]
        return picture
    except:
        picture=img1[y:y1,:]
        return picture



pic='sample (3).jpg'
abc=cv2.imread("sample (3).jpg")
img=differnece(abc)
print(img)