"Calculate sharpness of image"
from pathlib import Path
import cv2 as cv
import numpy as np

def variance_of_laplacian(image):
    """
    compute the Laplacian of the image and then return the focus measure, which is simply the variance of the Laplacian
    """
    res = cv.Laplacian(image, cv.CV_64F).var()
    #res = cv.Laplacian(image,)
    return res

def calc_sharpnes(img):
    "return the sharpness as an integer btween 0 and 100?"
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    a = variance_of_laplacian(grey)
    #print (a)
    return a

def gen_sharpness_picture(img):
    "generate a picture showing sharpness areas in image"
    cv.imshow("img", img)
    print("shape", img.shape)
    calc_size = 50
    h,  w = img.shape[:2]
    res = np.zeros((h,w),dtype=np.ubyte)

    for x in range(w-calc_size):
        for y in range(h-calc_size):
            area = img[y:y+calc_size, x:x+calc_size]
            val = calc_sharpnes(area)
            val = val//10
            if val>255:
                val=255
            res[y,x]= val
            #print (x, val, val//12)

    cv.imshow("area", res)

    cv.waitKey()

    return
 
    nn = 0
    #print(img)
    for x in range(n):
        for y in range(n):
            print ("x", x*wp, "y", y*hp)
            iarr = img[x*wp:wp, y*hp:hp]
            print("sha", iarr.shape)
            print(iarr)
            cv.imshow("uu"+str(nn), iarr )
            cv.waitKey(13000)
            nn += 1
    return False

if __name__ =='__main__':  
    picture1 = Path(__file__).parent / 'TestImages/piZ2_210907/1/color.jpg'
    picture2 = Path(__file__).parent / 'TestImages/piZ2_210907/2/color.jpg'
    picture3 = Path(__file__).parent / 'TestImages/zoom1/pic_04s.jpg'
    #print(picture1)
    #im1 = cv.imread(str(picture1))
    #calc_sharpnes(im1)
    #im2 = cv.imread(str(picture2))
    #calc_sharpnes(im2)
    im3 = cv.imread(str(picture3))
    res = gen_sharpness_picture(im3)
    #cv.imshow("res", res)
