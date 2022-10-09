import cv2
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)  # ignore UserWarning
try:
    from skimage.measure import compare_ssim as ssim  # compare_ssim fully deprecated in version 0.18
except ImportError:
    from skimage.metrics import structural_similarity as ssim


def processLaminate(masterURL, sampleURL):
    """
    [IMAGES] = <image of reference> <image(s) to compare with>
    """
    image1 = cv2.imread(masterURL)
    image2 = cv2.imread(sampleURL)

    master_img = image1
    copy_img = image2

    master_img_height = master_img.shape[0]
    master_img_width = master_img.shape[1]
    master_img_dim = (master_img_width, master_img_height)

    copy_img_height = copy_img.shape[0]
    copy_img_width = copy_img.shape[1]
    copy_img_dim = (copy_img_width, copy_img_height)

    if master_img_height < copy_img_height or master_img_width < copy_img_width:

        copy_img = cv2.resize(copy_img, master_img_dim)
    elif copy_img_height < master_img_height or copy_img_width < master_img_width:
        master_img = cv2.resize(master_img, copy_img_dim)

    images = list((master_img, copy_img))
    num_img = len(images)
    if num_img == 0:
        return {
            "isError": True,
            "message": "Something went wrong!",
            "exception": "No image received for image processing",
            "data": ""
        }
    if num_img < 2:
        print('Image of reference must be compared with, at least, one another image')
        return

    initialized = False
    ref_name = None
    ref_frame = None
    ref_gray_frame = None

    for image in images:
        frame = image  # extract the np.matrix
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # gray scale (from 3 RGB to 1 gray scale channel)

        if not initialized:  # initialisation with the first image
            ref_frame = frame
            ref_gray_frame = gray
            initialized = True
        else:
            # quantitative approach to determine the exact discrepancies between images
            # using the Structural Similarity Index (SSIM) - cf. ./ressources/

            (score, diff) = ssim(ref_gray_frame, gray, full=True)  # compute ssim between two images5.

            diff = (diff * 255).astype(
                "uint8")  # to detect contours, must be converted to  8-bit unsigned integers array in the [0,255] range
            retval, thresh = cv2.threshold(diff, 127, 255, cv2.THRESH_BINARY_INV)  # binarize image to find the contours
            contours, hirarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            temp_ref_frame = ref_frame.copy()
            filled_after = ref_frame.copy()
            mask = np.zeros(temp_ref_frame.shape, dtype='uint8')

            for contour in contours:  # adding a bounding box around the differences
                area = cv2.contourArea(contour)
                if area > 40:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(temp_ref_frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
                    cv2.rectangle(frame, (x - 3, y - 3), (x + w + 3, y + h + 3), (0, 0, 0), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
                    cv2.drawContours(mask, [contour], 0, (0, 255, 0), -1)
                    cv2.drawContours(filled_after, [contour], 0, (0, 255, 0), -1)

    return score * 100, frame


score, frame = processLaminate("D:\Pythonworks\Services\master222_1.jpg", "D:\Pythonworks\Services\sample222_11.jpg")
cv2.imwrite("scannedLaminated.jpg", frame)
print(score)