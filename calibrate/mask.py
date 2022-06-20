"""Find mask for picture"""
from pathlib import Path
from PIL import Image, ImageStat, ImageFilter #, ImageEnhance, ImageDraw,
#from api.device_config import read_device_config, save_device_config

CALIBRATE_SECTION = 'calibrate'

def create_mask(pathname, blur=False, tolerence=0.85):
    color = Image.open(pathname)
    if blur:
        grey = color.convert('L')
        #img = grey.filter(ImageFilter.MedianFilter(size=50))
        img = grey.filter(ImageFilter.BoxBlur(100))
        #img.show()
    else:
        img = color.convert('L')
    stat = ImageStat.Stat(img)
    mean = stat.mean[0]
    # top
    x = img.width/2
    for y in range(int(img.height*0.2)):
        val = img.getpixel((x,y))
        if val > mean*tolerence:
            break
    top = y
    #bottom
    for y in range(img.height-1, int(img.height*0.8), -1):
        val = img.getpixel((x,y))
        if val > mean*tolerence:
            break
    button = y
    #left
    y = img.height/2
    for x in range(int(img.width*0.2)):
        val = img.getpixel((x,y))
        if val > mean*tolerence:
            break
    left = x
    for x in range(img.width-1, int(img.width*0.8), -1):
        val = img.getpixel((x,y))
        if val > mean*tolerence:
            break
    right = x
    return (left, top, right, button)

def save_mask(config, mask, label="flash_mask"):
    #config = read_device_config(device)
    if CALIBRATE_SECTION not in config.sections():
        config.add_section(CALIBRATE_SECTION)
    config[CALIBRATE_SECTION][label +'_left'] = str(mask[0])
    config[CALIBRATE_SECTION][label +'_top'] = str(mask[1])
    config[CALIBRATE_SECTION][label +'_right'] = str(mask[2])
    config[CALIBRATE_SECTION][label +'_bottom'] = str(mask[3])
    return config

def create_mask_in_config(file, config, label="flash_mask", blur=None):
    mask = create_mask(file, blur=blur)
    print ("Mask:", mask)
    return save_mask(config, mask, label=label)

if __name__ == "__main__":
    FILE = "data/device/b827eb05abc2/calibrate/calcamera/flash.jpg"
    mymask = create_mask(Path(FILE))
    print (mymask)
    save_mask("123", mymask)
