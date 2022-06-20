"find objects in image"
from pathlib import Path
import cv2
import numpy as np

_DEBUG = True

def prepare_image(img):
    "prepare image for contour detections"
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(gray_img,5)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(median, -1, sharpen_kernel)
    thresh = cv2.threshold(sharpen, 50, 255, cv2.THRESH_BINARY_INV)[1] # org 160
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    #close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    if _DEBUG:
        cv2.imshow('color', img)
        cv2.imshow('gray', gray_img)
        #cv2.imshow('median', median)
        cv2.imshow('sharp', sharpen)
        cv2.imshow('thres', thresh)
    return thresh

def prepare_simple_image(img):
    "prepare image for contour detections"
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(gray_img,5)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(median, -1, sharpen_kernel)

    thresh = cv2.threshold(sharpen, 220, 255, cv2.THRESH_BINARY_INV)[1] # org 160
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    #close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    if _DEBUG:
        cv2.imshow('color', img)
        cv2.imshow('gray', gray_img)
        #cv2.imshow('median', median)
        cv2.imshow('sharp', sharpen)
        cv2.imshow('thres', thresh)
    return thresh


def find_contours(img):
    "find and display contours"
    image, contours, hierachy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("image", image)
    print("contours", contours)
    print("hiarachy", hierachy)
    


def find_rectangle(imagefile):
    "Find rectangle in an image"
    if not imagefile.exists():
        print("file does not exist:", imagefile)
        return None, None
    img = cv2.imread(str(imagefile))
    rows, cols, bands = img.shape
    if _DEBUG:
        print(f"width {rows} height {cols} bands {bands}")
    thresh = prepare_simple_image(img)
    cnts, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # thresh = prepare_image(img)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    # # Find contours and filter using threshold area
    # cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    max_area = rows * cols *0.95
    min_area = max_area * 0.1
    if _DEBUG:
        print("Area (max,min)", max_area, min_area)
    rectangle_number = 0
    rect_list = []
    print("hierachy",hierachy)
    for c in cnts:
        print("Contoure", c)
        area = cv2.contourArea(c)
        if _DEBUG:
            print("Area", area)
        if area > min_area:  # and area < max_area:
            x,y,w,h = cv2.boundingRect(c)
            if _DEBUG:
                print ("bounding rect", x,y,w,h)
                print("C",c)
            ROI = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(img, c, 0, (0,0,0), 15)
            rectangle_number += 1
            rect_list.append((x,y,w,h))
    if _DEBUG:
        print ("Shape:", img.shape)
        cv2.imshow('color2', img)
        # cv2.imshow('gray', gray_img)
        # cv2.imshow('median', median)
        # cv2.imshow('sharp', sharpen)
        # cv2.imshow('thres', thresh)
        #print ("kernel", kernel)
        print("antal rectangler", rectangle_number)
        print (rect_list)
        cv2.waitKey()
    return (cols,rows), rect_list

if __name__ == "__main__":
    picturefile = Path(__file__).parent / 'TestData/picture10s.jpg'
    picturefile = Path(__file__).parent / 'TestData/skraa.jpg'
    size, rectangles = find_rectangle(picturefile)
    print ("imagesize:", size, "rectangles", rectangles)
    