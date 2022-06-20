from cv2 import imread
from api.device_config import read_device_config, save_device_config, _read_config
from compute.settings import DEVICE_PATH
import cv2 as cv
import numpy as np


def read_mtx(device):
    config = read_device_config(device)
    if "camera" not in config.sections():
        print ("No camera matrix")
        return None
    #mtx = [[0 for x in range(3)] for y in range(3)] 
    mtx = np.empty((3,3))
    mtx[0][0] = float(config['camera']['fx'])
    mtx[1][1] = config['camera']['fy'] 
    mtx[1][0] = config['camera']['s']
    mtx[0][2] = config['camera']['cx']
    mtx[1][2] = config['camera']['cy']
    mtx[2][2] = 1
    dist = np.empty((5))
    dist[0] = config['camera']['dist0']
    dist[1] = config['camera']['dist1']
    dist[2] = config['camera']['dist2']
    dist[3] = config['camera']['dist3']
    dist[4] = config['camera']['dist4']
    #print('mtx',mtx)
    #save_device_config(config, device)
    return mtx, dist


def transform_picture(img, mtx, dist):
    #img = cv.imread('left12.jpg')
    cv.imshow('org', img)
    cv.waitKey(10000)
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # This is the easiest way. Just call the function and use ROI obtained above to crop the result.
    # # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    cv.imshow("dst", dst)    # crop the image
    x, y, w, h = roi
    dst2 = dst[y:y+h, x:x+w]
    #cv.imshow('org', img)
    cv.imshow("corr1", dst2)
    cv.waitKey(10000)
    #cv.imshow("corr2",dst2)
    # cv.imwrite('calibresult.png', dst)  
    return dst 

device = "1234"
m,d = read_mtx(device)
print(m)
print (d)
img =imread('calibrate/camera/testimages/danwand/serie2/picture_003.jpg')
dummy = transform_picture(img,m,d)
