"camera calibration"
#import glob
from pathlib import Path
import numpy as np
import cv2 as cv
from api.device_config import read_device_config, save_device_config
#from compute.settings import BASE_DIR
 
_DEBUG = False
 
def save_device_camera_matrix(device, mtx, dist):
    config = read_device_config(device)
    if "camera" not in config.sections():
        print ("adding section")
        config.add_section("camera")
    print("mtx", mtx)
    config['camera']['fx'] = str(mtx[0][0])
    config['camera']['fy'] = str(mtx[1][1])
    config['camera']['s'] = str(mtx[1][0])
    config['camera']['cx'] = str(mtx[0][2])
    config['camera']['cy'] = str(mtx[1][2])
    config['camera']['dist0'] = str(dist[0][0])
    config['camera']['dist1'] = str(dist[0][1])
    config['camera']['dist2'] = str(dist[0][2])
    config['camera']['dist3'] = str(dist[0][3])    
    config['camera']['dist4'] = str(dist[0][4])
    print('dist',dist)
    save_device_config(config, device)

def get_minimal_camera_matrix(mtx, dist, size):
    #h,  w = img.shape[:2]
    h,w = size
    print(size, w, h)
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    return newcameramtx, roi

def get_maximal_camera_matrix(mtx, dist, size):
    #h,  w = img.shape[:2]
    h,w = size
    print(size, w, h)
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
    return newcameramtx, roi

def undistort(img, mtx, dist):
    pass

def calibrate_camera(folder, chessboard=(6,8)):
    "calibrate by all jpg files in folder and used with a chess board gridx x gridy"
    if not Path(folder).exists():
        raise FileNotFoundError("The folder does not exist")
    #gridx = 6   # number point with full black corners
    #gridy = 8
    gridx = chessboard[0]
    gridy = chessboard[1]
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((gridx*gridy,3), np.float32)
    #objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    objp[:,:2] = np.mgrid[0:gridx,0:gridy].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    #find immages
    if _DEBUG:
        print("Folder:", folder)
        print("chessboard", chessboard)
    filemask = '*.jpg'
    images = folder.glob(filemask)
    ok_pictures = 0
    for fname in images:
        # if _DEBUG:
        #     print(fname)
        img = cv.imread(str(fname))
        alpha = 2.5 # Contrast control (1.0-3.0)
        beta = 00 # Brightness control (0-100)
        img2 = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
        #img2 = cv.resize(img,(img.shape[1]//3,img.shape[0]//3), interpolation = cv.INTER_AREA)
        gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
        #cv.imshow("grey", gray)
        #cv.waitKey(2000)
        if _DEBUG:
            #cv.imshow("image",img)
            # cv.imshow("gray",gray)
            # cv.waitKey(1000)
            pass
        # Find the chess board corners
        #ret, corners = cv.findChessboardCorners(gray, (gridx,gridy), None, flags=cv.CALIB_CB_ADAPTIVE_THRESH )        
        #ret, corners = cv.findChessboardCorners(gray, (gridx,gridy), None)
        ret, corners = cv.findChessboardCornersSB(gray, (gridx,gridy), None)
        #ret, corners = cv.findChessboardCorners(gray, (7,7), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            if _DEBUG:
                print("Corners found in", fname)
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            ok_pictures +=1
            if _DEBUG:            
                # Draw and display the corners
                cv.drawChessboardCorners(img, (gridx,gridy), corners2, ret)
                #cv.drawChessboardCorners(img, (7,7), corners2, ret)
                cv.imshow(str(fname.name), img)
                pic1 = fname
                #print(pic1)
                cv.waitKey(4500)
                cv.destroyWindow(str(fname.name))
        else:
            print("der er noget galt med ", str(fname.name))
            if _DEBUG:
                #cv.imshow(str(fname.name), img)
                #cv.waitKey(5000)
                pass
        if _DEBUG:
            cv.waitKey(1500)
            cv.destroyAllWindows()
    if _DEBUG:
        #print("imgpoints", imgpoints)
        cv.destroyAllWindows()

    # print(list(images))
    # if len(list(images))==0:
    #     if _DEBUG:
    #         print("No files found in folder")
    #     return None, None
    # calibration
    #print (objpoints)
    if len(objpoints)==0:
        return None,None
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    if _DEBUG:
        print("reprojection error",ret)
        print("camera matrix",mtx)
        print('distortion', dist)
        #print ('rotation vecs', rvecs)
        #print("tranlation vecs", tvecs)
        img = cv.imread(str(pic1))
        #img = cv.imread(FOLDER +'my/color1.jpg')
        h,  w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        print("newcameramtx", newcameramtx)
        #print("roi", roi)
        np.save("trans.npy", newcameramtx)
        # undistort
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imshow("org", img)
        cv.imshow("result", dst)
        cv.waitKey(5000)
        cv.destroyAllWindows()
    #cv.imwrite('calibresult.png', dst)
    #print ("Results", mtx, dist, rvecs, tvecs)
    print("Ok pictures:", ok_pictures)
    return mtx, dist