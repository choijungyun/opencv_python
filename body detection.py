import urllib
from urllib.request import urlopen
import cv2
import numpy as np
import math
import requests


#url = "http://203.252.195.136/image.php"
#html_result = requests.get(url)
#lay = html_result.text

lay = 'wed.png'

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

body_cascade = cv2.CascadeClassifier('fullbody_detector.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

specs_ori = cv2.imread(lay, -1)
cigar_ori = cv2.imread('wed2.png', -1)


face_x = 0
face_y = 0
face_w = 0
face_h = 0
 
def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image
 
    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src
 
 

# store the previous face coordinate
prev_fx = 0
prev_fy = 0
prev_fw = 0
prev_fh = 0

while (cap.isOpened()):
    # read image
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # if ret == True:
    #   img = cv2.flip(img, 1)
    # get hand data from the rectangle sub window on the screen

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    fx = 0; fy = 0; fw = 0; fh = 0
    for (fx, fy, fw, fh) in faces:
        if ((abs(prev_fx - fx) > 10) and (abs(prev_fy-fy) > 10)):
            prev_fx = fx; prev_fy = fy; prev_fw = fw; prev_fh = fh;
        else:
            fx = prev_fx; fy = prev_fy; fw = prev_fw; fh = prev_fh;

        cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), (255, 255, 220), 2)

        face_w = fw
        face_h = fh
        face_x1 = fx
        face_x2 = face_x1 + face_h
        face_y1 = fy
        face_y2 = face_y1 + face_h

        img_path = lay
        imgDress = cv2.imread(img_path, -1)
        orig_mask = imgDress[:, :, 3]
        orig_mask_inv = cv2.bitwise_not(orig_mask)
        imgDress = imgDress[:, :, 0:3]
        origLogoHeight, origLogoWidth = imgDress.shape[:2]
        ret, img = cap.read()
        img_h, img_w = img.shape[:2]


        # resize original dress image to fit the camera image
        dressWidth = 3 * face_w
        dressHeight = int(dressWidth * origLogoHeight / origLogoWidth)

        shirt_x1 = face_x2 - int(face_w / 2) - int(dressWidth / 2)
        shirt_x2 = shirt_x1 + dressWidth
        shirt_y1 = face_y2 + 5
        shirt_y2 = shirt_y1 + dressHeight

        dressWidth = shirt_x2 - shirt_x1
        dressHeight = shirt_y2 - shirt_y1

        if dressWidth < 0 or dressHeight < 0:
            continue

        dress = cv2.resize(imgDress, (dressWidth, dressHeight), interpolation=cv2.INTER_AREA)


        # adjust the image to fit into the camera image, to prevent window size overflow
        if shirt_x1 < 0:
           shirt_x1 = 0
        if shirt_y1 < 0:
           shirt_y1 =0
        if shirt_x2 > img_w:
           shirt_x2 = img_w
        if shirt_y2 > img_h:
           shirt_y2 = img_h

        # calculate the cropped image size
        crop_dressWidth = shirt_x2 - shirt_x1
        crop_dressHeight = shirt_y2 - shirt_y1
       # print("w=%d, h=%d, cw=%d, ch=%d" % (dressWidth, dressHeight, crop_dressWidth, crop_dressHeight))

        # resize the original dress mask with the current enlarged image size
        mask = cv2.resize(orig_mask, (dressWidth, dressHeight), interpolation=cv2.INTER_AREA)
        mask_inv = cv2.resize(orig_mask_inv, (dressWidth, dressHeight), interpolation=cv2.INTER_AREA)
        #print("x1=%d, y1=%d, x2=%d, y2=%d" % (shirt_x1, shirt_y1, shirt_x2, shirt_y2))

        mask = mask[0:crop_dressHeight, 0:crop_dressWidth]
        mask_inv = mask_inv[0:crop_dressHeight, 0:crop_dressWidth]

        cv2.imshow("mask", mask)
        cv2.imshow("mask_inv", mask_inv)

        crop_dress = dress[0:crop_dressHeight, 0:crop_dressWidth]
        roi = img[shirt_y1:shirt_y2, shirt_x1:shirt_x2]
        roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        roi_fg = cv2.bitwise_and(crop_dress, crop_dress, mask=mask)
        dst = cv2.add(roi_bg, roi_fg)
        img[shirt_y1:shirt_y2, shirt_x1:shirt_x2] = dst
        break
#얼굴 안잡힐 때 드레스 띄우는 코드 추가
    face_glass_roi_color = img[100:200, 10:200]
    face_cigar_roi_color = img[200:300, 10:100]


    sh_glass = 100
    sh_cigar = 100
    specs = cv2.resize(specs_ori, (10, 100), interpolation=cv2.INTER_CUBIC)
    cigar = cv2.resize(cigar_ori, (10, 100), interpolation=cv2.INTER_CUBIC)
    transparentOverlay(face_glass_roi_color, specs)
    transparentOverlay(face_cigar_roi_color, cigar)


    cv2.rectangle(img, (0, 100), (100, 200), (0, 255, 0), 0)
    crop_img = img[100:200, 0:100]
    cv2.rectangle(img, (0, 200), (100, 300), (255, 255, 255), 0)
    crop_img = img[100:300, 0:200]
    cv2.rectangle(img, (0, 300), (100, 400), (255, 255, 255), 0)
    crop_img = img[100:400, 0:300]

    #Button rectangle
    cv2.rectangle(img,(1180,100),(1280,200),(255,0,0),2)
    crop_img2 = img[100:200, 1180:1280]



    # convert to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    grey2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)
    # applying gaussian blur
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)

    # thresholdin: Otsu's Binarization method
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    _, thresh2 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # show thresholded image
    cv2.imshow('Thresholded', thresh1)
    cv2.imshow('Thresholded', thresh2)

    # check OpenCV version to avoid unpacking error
    (version, _, _) = cv2.__version__.split('.')

    if version == '3':
        image, contours, hierarchy = cv2.findContours(thresh1.copy(),\
                                                      cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    elif version == '2':
        contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, \
                                               cv2.CHAIN_APPROX_NONE)



    # find contour with max area
    cnt = max(contours, key=lambda x: cv2.contourArea(x))

    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)
    cv2.rectangle(crop_img2, (x, y), (x + w, y + h), (0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt)

    # drawing contours
    drawing = np.zeros(crop_img.shape, np.uint8)
    drawing2 = np.zeros(crop_img2.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
    cv2.drawContours(drawing2, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing2, [hull], 0, (0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
    cv2.drawContours(thresh2, contours, -1, (0, 255, 0), 3)

    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

        # apply cosine rule here
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
            cv2.circle(crop_img2, far, 1, [0, 0, 255], -1)

        # dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.line(crop_img, start, end, [0, 255, 0], 2)
        cv2.line(crop_img2, start, end, [0, 255, 0], 2)
        # cv2.circle(crop_img,far,5,[0,0,255],-1)
    if count_defects == 1:
        str = "This is a basic hand gesture recognizer"
        cv2.putText(img, str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

    elif count_defects == 2:
        str = "This is a basic hand gesture recognizer"
        cv2.putText(img, str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 3:
        lay = 'wed2.png'

    elif count_defects == 4:
        cv2.putText(img,"Hi!!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    else:
        cv2.putText(img,"Hello World!!!", (50, 50),\
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2)



    # show appropriate images in windows
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    all_img2 = np.hstack((drawing2, crop_img2))
    cv2.imshow('Contours', all_img)
    cv2.imshow('Contours2', all_img2)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
