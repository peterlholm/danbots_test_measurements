"""
flash test
"""
from os import makedirs
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageStat, ImageFilter #, ImageEnhance ImageDraw,
#from configparser import ConfigParser
#from api.views import device_folder
from compute.settings import DEVICE_PATH
from api.device_config import read_device_config, save_device_config

FOLDER = "calibrate/testdata/"
FOLDER = "data/device/b827eb05abc2/calibrate"
FILE_NAME = "flash01.jpg"
CALIBRATE_SECTION = 'calibrate'
LED_LIGHT_CORR = 'led_corr.png'
CENTER_AREA = 0.3   # the part to be excluded


_DEBUG =True

file = Path(FOLDER+FILE_NAME)

def read_config_section(device):
    config = read_device_config(device)
    config = read_device_config('123')
    #print(config.sections())
    if CALIBRATE_SECTION not in config.sections():
        print ("adding section")
        config.add_section(CALIBRATE_SECTION)
    #cal_section = config[CALIBRATE_SECTION]
    # print(cal_section.items())
    # for key in cal_section.items():
    #     print (key)
    return config

def save_config(config):
    save_device_config(config, "123")

def create_mask(img):
    if img.mode != "L":
        grey = img.convert('L', )
    else:
        grey = img
    # enhancer = ImageEnhance.Contrast(grey)
    # enh = enhancer.enhance(3)
    # enh.show()
    # korr = grey.filter(ImageFilter.MedianFilter(size=31))
    # korr.show()
    mask = Image.new('L', grey.size, color=255)
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            if (x >grey.width * 0.90) or (y >grey.height*0.85):
                mask.putpixel((x,y), 0)
            # if korr.getpixel((x,y))[0] < 20:
            #     mask.putpixel((x,y), 0)
    # grey.show()
    # korr7 = grey.filter(ImageFilter.MedianFilter(size=31))
    # korr7.show()
    # mask.show()
    return mask

# def flash_led_test(device="123"):
#     print ("start flash led test", datetime.now())
#     device_folder = DEVICE_PATH / device / "calibrate/calflash"
#     makedirs(device_folder, exist_ok=True)
#     config = read_config_section(device)
#     img = Image.open(device_folder / FILE_NAME)
#     if _DEBUG:
#         print("Input:", img.size, img.mode)
#         img.show()
#     grey = img.convert('L')
#     mask = create_mask(grey)
#     grey.putalpha(mask)
#     grey.show()

#     #  # reduse resolution
#     # rimg = img.resize((160,120))   #
#     # #rimg.show()
#     # grey = rimg.convert('L')
#     # #grey.show()


#     #grey.show()
#     # width = grey.width
#     # height = grey.height

#     # # calculate mean from center area
#     # reduce = 0.30
#     # rect = (width*reduce/2, height*reduce/2, width*(1-reduce/2), height*(1-reduce/2))
#     # mask2 = Image.new('L', grey.size, color=0)
#     # draw = ImageDraw.Draw(mask)
#     # draw.rectangle(rect,fill=255)

#     mean = int(ImageStat.Stat(grey).mean[0])
#     print("mean", mean)

#     return
#     grey.putalpha(mask2)
#     grey.show()
#     return
#     mean = int(ImageStat.Stat(grey).mean[0])
#     print("mean", mean)

#     print (datetime.now())
#     # restore image
#     grey = rimg.convert('L')
#     korr = Image.new('L', grey.size)
#     print ("new",datetime.now())
#     for x in range(0, grey.width):
#         for y in range(0, grey.height):
#             val = mean - grey.getpixel((x,y)) + COMP_OFFSET
#             korr.putpixel((x,y), val )
#     print ("filter", datetime.now())
#     korr.show()
#     korr.save(device_folder / "korr.png")
#     korr1 = korr.filter(ImageFilter.MedianFilter(size=3))
#     korr1.show()
#     korr1.save(device_folder / "korr1.png")
#     korr7 = korr.filter(ImageFilter.MedianFilter(size=7))
#     korr7.save(device_folder / "korr7.png")
#     korr7.show()
#     medkorr = korr.filter(ImageFilter.MedianFilter(size=31))
#     print ("calc", datetime.now())
#     medkorr.show()
#     medkorr.save(device_folder / LED_LIGHT_CORR)
#     if _DEBUG:
#         repair = Image.new('L', grey.size)
#         for x in range(0, repair.width):
#             for y in range(0, repair.height):
#                 val = grey.getpixel((x,y)) + (medkorr.getpixel((x,y)) - COMP_OFFSET)
#                 #print(val)
#                 repair.putpixel((x,y), val )
#         #repair.show()

#     config[CALIBRATE_SECTION]['flash_calibration'] = '1'
#     config[CALIBRATE_SECTION]['light_correction'] = LED_LIGHT_CORR
#     config[CALIBRATE_SECTION]['light_mask'] = "light_mask.png"
#     save_config(config)
#     return True

def gen_flash_correction(device="123"):
    # generate a diff and a mult correction matrix for a total white image
    MEDIAN_FILTER_SIZE = 3 # 7, 31
    COMP_OFFSET = 200
    device_calc_folder = DEVICE_PATH / device / 'calibrate'
    device_data_folder =device_calc_folder / "calflash"
    makedirs(device_calc_folder, exist_ok=True)
    config = read_config_section(device)
    img = Image.open(device_data_folder / FILE_NAME)
    if _DEBUG:
        print("Input:", img.size, img.mode)
    grey = img.convert('L')
    mean = ImageStat.Stat(grey).mean[0]
    imean = int(mean)
    korr = Image.new('L', grey.size)
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            val = imean - grey.getpixel((x,y)) + COMP_OFFSET
            korr.putpixel((x,y), val )
    korr.save(device_data_folder / "diff.png")
    korr1 = korr.filter(ImageFilter.MedianFilter(size=MEDIAN_FILTER_SIZE))
    korr1.save(device_data_folder / "korr_median.png")
    korr1.save(device_calc_folder / LED_LIGHT_CORR)
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            val = grey.getpixel((x,y))/mean * 10 + COMP_OFFSET
            korr.putpixel((x,y), int(val) )
    korr.save(device_data_folder / "mult.png")
