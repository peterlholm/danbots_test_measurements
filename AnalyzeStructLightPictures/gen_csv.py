from os import path
import numpy as np
from pathlib import Path
from PIL import Image
import cv2

DATAFOLDER = "data"
FILENAME="blender"
INPUTFILE = Path(DATAFOLDER) / (FILENAME+".png")
COL =80

def make_grayscale(img):
    # Transform color image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

def normalize_image255(img):
    # Changes the input image range from (0, 255) to (0, 1)number_of_epochs = 5
    img = img/255.0
    return img


def gen_nn():
    image1 = cv2.imread(str(high), 1).astype(np.float32)
    #black = folder + 'image9.png' #'' blenderblack.png
    #image2 = cv2.imread(black,1).astype(np.float32)
    image = image1 #- image2
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)

def gen_csv():  
    img = Image.open(INPUTFILE)
    grey = img.convert('L')
    f = open(FILENAME+".csv", "w")
    image1 = cv2.imread(str(INPUTFILE), 1).astype(np.float32)
    image = image1
    inp_1 = normalize_image255(image)
    # cv2.imwrite('image.png', image)
    # cv2.imwrite('image1.png', inp_1)   
    # inp_2 = make_grayscale(inp_1)
    # cv2.imwrite('image2.png', inp_2)   
    
    f.write('"y","R","G","B","L","cR","cG","cB","normR","normG","normB","cL"\n')

    x=COL
    
    print("Bands", img.getbands())
    for y in range(0, img.height):
        pic = img.getpixel((x,y))
        g = grey.getpixel((x,y))
        print("pic", pic)
        print("i",image[y,x])
        print("i2",inp_1[y,x])
        f.write(f'{y},{pic[0]},{pic[1]},{pic[2]},{g},{image[y,x,2]},{image[y,x,1]},{image[y,x,0]},{inp_1[y,x,2]},{inp_1[y,x,1]},{inp_1[y,x,0]}\n')

        # print("i2",inp_1[y,x])
        # print("i3",inp_2[y,x])
    
    
    f.close()
     

gen_csv()
