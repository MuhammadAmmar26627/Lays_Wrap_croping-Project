# import streamlit as st
# import cv2
# import numpy as np
# st.title('image crop')
# uploaded_file=st.file_uploader('Image',['png', 'jpg','jpeg'])
# img1=uploaded_file.read()
# # img1=cv2.imread(img)
# # print(np.array(img))

# if uploaded_file:
#     img1=uploaded_file.read()
#     print(img1)
#     st.image(uploaded_file)
#     # st.write(img1)


import cv2
import numpy as np
import streamlit as st
import PIL.Image as Image
import numpy as np
import imutils
from math import atan,degrees

uploaded_file = st.file_uploader("Choose a image file", type=['png', 'jpg','jpeg'])
print(uploaded_file)
if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    # Now do something with the image! For example, let's display it:
    st.image(opencv_image, channels="BGR")
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
        # cv2.circle(img=rot, center = (x,y), radius =5, color =(0,255,0), thickness=10)
        # cv2.circle(img=rot, center = (x1,y1), radius =5, color =(0,255,0), thickness=10)
        st.write(theta)
        st.image(rot,channels='BGR')
        hsv=cv2.cvtColor(rot,cv2.COLOR_BGR2HSV)
        mask_image=cv2.inRange(hsv[:,:int(np.shape(hsv)[1]/5)],np.array((0,0,0)),np.array((180,255,bright)))
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
                print(len(a))
                if len(a)==2:
                    break
        try:
            box_image= box_image[y:y1,:]
        except:
            box_image= box_image[y1:y,:]
        st.image(box_image,channels='BGR')

    # btn = st.download_button(
    #   label="Download image",
    #   data=uploaded_file,
    #   file_name="imagename.png",
    #   mime="image/png")    




    
    # btn = st.download_button(
    #         label="Download image",
    #         data=uploaded_file,
    #         file_name="flower.png",
    #         mime="image/png"
    #       )