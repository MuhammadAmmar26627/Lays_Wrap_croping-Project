# from skimage.metrics import structural_similarity as compare_ssim
from skimage.metrics import structural_similarity as compare_ssim
import imutils
import cv2
import numpy as np
# load the two input images

imageA = cv2.imread('3_1.jpg')
# imageA=image[:,:-4]
imageB = cv2.imread('4_1.jpg')
print(np.shape(imageA),np.shape(imageB))
if np.shape(imageA)[0]>np.shape(imageB)[0]:
    imageA = imageA[:np.shape(imageB)[0],:]
elif np.shape(imageA)[0]<np.shape(imageB)[0]:
    imageB = imageB[:np.shape(imageA)[0],:]
elif np.shape(imageA)[1]>np.shape(imageB)[1]:
    imageA = imageA[:,:np.shape(imageB)[1]]
else:
    imageB = imageB[:,:np.shape(imageA)[1]]
print(np.shape(imageA),np.shape(imageB))
# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
try:
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # cv2.drawContours(imageA, cnts, -1, (0,255,0), 1)
    # loop over the contours
    for c in cnts:
    #     # compute the bounding box of the contour and then draw the
    #     # bounding box on both input images to represent where the two
    #     # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 1)
    cv2.drawContours(imageA, cnts, -1, (0, 255, 0), 1)
    cv2.drawContours(imageB, cnts, -1, (0, 255, 0), 1)
    #     cv2.drawContours(imageA, c, -1, (0,255,0), 1)
    #     cv2.drawContours(imageB, c, -1, (0,255,0), 1)
    # show the output images
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)
    # run
    # python image_diff.py --first 3_1.jpg --second 4_1.jpg
except:
    pass