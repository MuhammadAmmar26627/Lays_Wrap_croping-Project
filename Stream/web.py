import cv2
import numpy as np
import streamlit as st
import PIL.Image as Image
import numpy as np
import imutils
from math import atan,degrees
import base64
from io import BytesIO

uploaded_file = st.file_uploader("Choose a image file", type=['png', 'jpg','jpeg'])
if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    # Now do something with the image! For example, let's display it:
    st.image(opencv_image, channels="BGR")
    genre = st.radio(
            "What is backgroung colour",
            ('pink', 'White'))

    bright=st.slider('Select Brightness',15,55,value=27)
    hsv=cv2.cvtColor(opencv_image,cv2.COLOR_BGR2HSV)
    mask_image=cv2.inRange(hsv[:,:int(np.shape(hsv)[1]/5)],np.array((0,0,0)),np.array((180,255,bright)))
    contour,hierarchy=cv2.findContours(mask_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    contour=sorted(contour,key=lambda x:cv2.contourArea(x),reverse=True)
    a=[]
    box_image=opencv_image.copy()
    a=[]
    for cnt in contour:
        area=cv2.contourArea(cnt)
        # (x,y,w,h)=cv2.boundingRect(cnt)
        # cv2.rectangle(opencv_image,(x,y),(x+w,y+h),(0,255,0),2)
        if (area>22000) & (area<26000):
#             print(area)
            a.append(cnt)
# #             cv2.drawContours(img, cnt, -1, (0, 255, 0), 10)
            (x,y,w,h)=cv2.boundingRect(cnt)
            cv2.rectangle(box_image,(x,y),(x+w,y+h),(0,255,0),2)
            print(len(a))
            if len(a)==2:
                break
    # st.image(opencv_image[:,:,::-1])
    st.image(box_image,channels='BGR')
    if st.button('Next'):
        x,y,w,h = cv2.boundingRect(a[0])
        x1,y1,w1,h1 = cv2.boundingRect(a[1])
        
        height=int(x)-int(x1)
        base=int(y)-int(y1)
        theta=atan(height/base)
        theta= degrees(theta)
        img=opencv_image.copy()


        rot=imutils.rotate(img,angle=-theta)
        img1=rot.copy
        # genre = st.radio(
        #     "What is backgroung colour",
        #     ('pink', 'White'))

        if genre == 'pink':
            hsv=cv2.cvtColor(rot,cv2.COLOR_BGR2HSV)
            mask_image=cv2.inRange(hsv,np.array((125,100,30)),np.array((255,255,255)))
            contour,hierarchy=cv2.findContours(mask_image,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
            contour=sorted(contour,key=lambda x:cv2.contourArea(x),reverse=True)
            x,y,w,h = cv2.boundingRect(contour[1])
            # cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
            rot=rot[y:y+h,x:x+w]
            st.write('You selected comedy.')
        else:
            hsv=cv2.cvtColor(rot,cv2.COLOR_BGR2HSV)
            mask_image=cv2.inRange(hsv,np.array((0,0,0)),np.array((255,25,255)))
            contour,hierarchy=cv2.findContours(mask_image,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
            contour=sorted(contour,key=lambda x:cv2.contourArea(x),reverse=True)
            x,y,w,h = cv2.boundingRect(contour[1])
            # cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
            rot=rot[y:y+h,x:x+w]
            st.write("You didn't select comedy.")



        # cv2.circle(img=rot, center = (x,y), radius =5, color =(0,255,0), thickness=10)
        # cv2.circle(img=rot, center = (x1,y1), radius =5, color =(0,255,0), thickness=10)
        st.write(theta)
        st.image(rot,channels='BGR')

        bright1=st.slider('Confirm Brightness',15,55,value=bright)
        hsv=cv2.cvtColor(rot,cv2.COLOR_BGR2HSV)
        mask_image=cv2.inRange(hsv[:,:int(np.shape(hsv)[1]/5)],np.array((0,0,0)),np.array((180,255,bright1)))
        contour,hierarchy=cv2.findContours(mask_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        contour=sorted(contour,key=lambda x:cv2.contourArea(x),reverse=True)
        a=[]
        box_image=rot.copy()

        a=[]
        for cnt in contour:
            area=cv2.contourArea(cnt)
            # (x,y,w,h)=cv2.boundingRect(cnt)
            # cv2.rectangle(opencv_image,(x,y),(x+w,y+h),(0,255,0),2)
            if (area>22000) & (area<26000):
    #             print(area)
                a.append(cnt)
    # #             cv2.drawContours(img, cnt, -1, (0, 255, 0), 10)
                (x,y,w,h)=cv2.boundingRect(cnt)
                cv2.rectangle(box_image,(x,y),(x+w,y+h),(0,255,0),2)
                # print(len(a))
                if len(a)==2:
                    break
        st.write(len(a))
        st.image(box_image,channels='BGR')
        x,y,w,h = cv2.boundingRect(a[0])
        x1,y1,w1,h1 = cv2.boundingRect(a[1])
        st.write(y,y1)
        st.write(rot.shape)
        if y>y1:
            box_image= rot[y1:y,:]
            st.write(f'{box_image.shape}0')
        else:
            box_image= rot[y:y1,:]
            st.write(f'{box_image.shape}1')  
        st.image(box_image,channels='BGR')



        image_bytes = cv2.imencode('.jpg', box_image)[1].tobytes()
        btn = st.download_button(
            label="Download image",
            data=image_bytes,
            file_name="flower.png",
            mime="image/png")