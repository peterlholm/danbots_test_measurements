"Calculate distance to target"
from math import tan, pi
import cv2
import numpy as np
from compute.settings import BASE_DIR

_DEBUG = False

def find_rectangle(imagefile):
    "Find rectangle in an image"
    img = cv2.imread(str(imagefile))
    rows, cols, bands = img.shape
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(gray_img,5)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(median, -1, sharpen_kernel)
    thresh = cv2.threshold(sharpen, 60, 255, cv2.THRESH_BINARY_INV)[1] # org 160
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    # Find contours and filter using threshold area
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    max_area = rows * cols *0.95
    min_area = max_area * 0.1
    if _DEBUG:
        print("Area (max,min)", max_area, min_area)
    rectangle_number = 0
    rect_list = []
    for c in cnts:
        area = cv2.contourArea(c)
        if _DEBUG:
            print("Area", area)
        if area > min_area and area < max_area:
            x,y,w,h = cv2.boundingRect(c)
            if _DEBUG:
                print ("rect", x,y,w,h)
                #print("C",c)
            ROI = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 2)
            rectangle_number += 1
            rect_list.append((x,y,w,h))
    if _DEBUG:
        print ("Shape:", img.shape)
        cv2.imshow('color', img)
        cv2.imshow('gray', gray_img)
        cv2.imshow('median', median)
        cv2.imshow('sharp', sharpen)
        cv2.imshow('thres', thresh)
        print ("kernel", kernel)
        print("antal rectangler", rectangle_number)
        print (rect_list)
        cv2.waitKey()
    return (cols,rows), rect_list

def rect2dist(rectsize, imgheight):
    "calculate distance from 1cm square"
    FOV = 48    # grader
    FOV_80 = 39 # 0.8 zoom
    OBJ_DIST =1.8
    #print("rectsixe",rectsize, "Image height", imgheight)
    imgsize = imgheight/rectsize *10 # mm
    height = imgsize/2 /tan(FOV/180*pi/2) - OBJ_DIST   # mm
    return height   # in mm

def calc_dist(imagefile):
    size, rectlist = find_rectangle(imagefile)
    print("Rectlist", rectlist)
    print("size", size)
    myrect = None
    for r in rectlist:
        print(r)
        if r[0]>10 or r[1]>10:
            if r[2]>r[3]*0.9 and r[2]<r[3]*1.1:
                myrect = r
                break
    
    if myrect is None:
        print("rect ikke fundet")
        return False
    
    rectsize = (myrect[2]+myrect[3])/2
    print("Size:", rectsize)
    height = rect2dist(rectsize, size[1])
    return str(height)+ " mm"
  
